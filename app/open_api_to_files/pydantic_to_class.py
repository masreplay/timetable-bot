import typing
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Type

import humps

T = typing.TypeVar("T")


@dataclass()
class ClassFile:
    name: str
    body: str


@dataclass
class DartConvertor:
    pydantic_class: T
    extension: str = ".dart"

    @staticmethod
    def enum(enum: Enum):
        file_name = f"{humps.decamelize(enum.__name__)}.dart"
        values = "\n\t".join([f'@JsonValue("{e.value}")\n\t{e.value};' for e in enum])
        enum_class = f"enum {enum.__name__} {{\n\t{values}\n}}"
        return ClassFile(file_name, enum_class)

    @staticmethod
    def __datatype__() -> Dict[Type, str]:
        return {
            str: "String",
            int: "Int",
            datetime: "DateTime",
            float: "double"
        }

    def constructor(self, is_const: bool = True):
        members = "\n"
        for v in self.pydantic_class.__fields__.values():
            members += f"\t\trequired this.{v.name},\n"
        return f'\t{"const " if is_const else ""}{self.name}({{{members}\t}});'

    @property
    def name(self) -> str:
        return self.pydantic_class.__name__

    @property
    def file_name(self) -> str:
        return self.name.lower() + ".dart"

    @property
    def generate(self) -> str:
        return f"part '{humps.decamelize(self.name)}.g.dart';\n\n" \
               f"@JsonSerializable(explicitToJson: true)\nclass {self.name} {{\n" \
               f"{self.body()}\n{self.constructor()}\n\n{self.from_and_to_json}" \
               f"\n}}"

    @property
    def file(self):
        return ClassFile(self.file_name, self.generate)

    @property
    def from_and_to_json(self):
        return f"\tfactory {self.name}.fromJson(Map<String, dynamic> json) =>\n" \
               f"\t\t\t_${self.name}FromJson(json);\n\n" \
               f"\tMap<String, dynamic> toJson() => _${self.name}ToJson(this);"

    def body(self):
        value = ""
        for k, v in self.pydantic_class.__fields__.items():
            annotation = f"@JsonKey(name: '{v.name}')"
            var_name = humps.camelize(v.name)
            var_type: str
            if v.type_ in self.__datatype__().keys():
                var_type = self.__datatype__()[v.type_]
            else:
                var_type = v.type_.__name__
            nullable = "" if v.required else "?"
            value += f'\t{annotation}\n\tfinal {var_type}{nullable} {var_name};\n'
        return value
