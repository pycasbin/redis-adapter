from casbin import persist
import redis
import json


class CasbinRule:
    """
    CasbinRule model
    """

    def __init__(
        self, ptype=None, v0=None, v1=None, v2=None, v3=None, v4=None, v5=None
    ):
        self.ptype = ptype
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.v5 = v5

    def dict(self):
        d = {"ptype": self.ptype}

        for value in dir(self):
            if (
                getattr(self, value) is not None
                and value.startswith("v")
                and value[1:].isnumeric()
            ):
                d[value] = getattr(self, value)

        return d

    def __str__(self):
        return ", ".join(self.dict().values())

    def __repr__(self):
        return '<CasbinRule :"{}">'.format(str(self))


class Adapter(persist.Adapter):
    """the interface for Casbin adapters."""

    def __init__(
        self, host, port, username=None, password=None, pool=None, key="casbin_rules"
    ):
        self.key = key
        self.client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            connection_pool=pool,
            decode_responses=True,
        )

    def drop_table(self):
        self.client.delete(self.key)

    def load_policy(self, model):
        """Implementing add Interface for casbin. Load all policy rules from redis

        Args:
            model (CasbinRule): CasbinRule object
        """

        length = self.client.llen(self.key)
        for i in range(length):
            line = self.client.lindex(self.key, i)
            line = json.loads(line)
            rule = CasbinRule(**line)
            persist.load_policy_line(str(rule), model)

    def _save_policy_line(self, ptype, rule):
        line = CasbinRule(ptype=ptype)
        for index, value in enumerate(rule):
            setattr(line, f"v{index}", value)
        self.client.rpush(self.key, json.dumps(line.dict()))

    def _delete_policy_lines(self, ptype, rule):
        line = CasbinRule(ptype=ptype)
        for index, value in enumerate(rule):
            setattr(line, f"v{index}", value)

        # if rule is empty, do nothing
        # else find all given rules and delete them
        if len(line.dict()) == 0:
            return 0
        else:
            self.client.lrem(self.key, 0, json.dumps(line.dict()))

    def save_policy(self, model) -> bool:
        """Implement add Interface for casbin. Save the policy in mongodb

        Args:
            model (Class Model): Casbin Model which loads from .conf file usually.

        Returns:
            bool: True if succeed
        """
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    self._save_policy_line(ptype, rule)
        return True

    def add_policy(self, sec, ptype, rule):
        """Add policy rules to redis

        Args:
            sec (str): Section name, 'g' or 'p'
            ptype (str): Policy type, 'g', 'g2', 'p', etc.
            rule (CasbinRule): Casbin rule will be added

        Returns:
            bool: True if succeed else False
        """
        self._save_policy_line(ptype, rule)
        return True

    def remove_policy(self, sec, ptype, rule):
        """Remove policy rules in redis(rules duplicate will all be removed)

        Args:
            sec (str): Section name, 'g' or 'p'
            ptype (str): Policy type, 'g', 'g2', 'p', etc.
            rule (CasbinRule): Casbin rule if it is exactly same as will be removed.

        Returns:
            bool: True if succeed else False
        """
        self._delete_policy_lines(ptype, rule)
        return True

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """Remove policy rules that match the filter from the storage.
           This is part of the Auto-Save feature.

        Args:
            sec (str): Section name, 'g' or 'p'
            ptype (str): Policy type, 'g', 'g2', 'p', etc.
            field_index (int): The policy index at which the filed_values begins filtering. Its range is [0, 5]
            field_values(List[str]): A list of rules to filter policy which starts from

        Returns:
            bool: True if succeed else False
        """
        if not (0 <= field_index <= 5):
            return False
        if not (1 <= field_index + len(field_values) <= 6):
            return False

        length = self.client.llen(self.key)
        for i in range(length):
            line = json.loads(self.client.lindex(self.key, i))
            if ptype != line.get("ptype"):
                continue
            j = 1
            is_match = False
            keys = list(line.keys())[field_index : field_index + len(field_values) + 1]
            for field_value in field_values:
                if field_value == line[keys[j]]:
                    j += 1
                    if j == len(field_values):
                        is_match = True
                else:
                    break
            if is_match:
                self.client.lset(self.key, i, "__CASBIN_DELETED__")

        self.client.lrem(self.key, 0, "__CASBIN_DELETED__")
        return True
