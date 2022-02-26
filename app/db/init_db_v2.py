import re
from uuid import uuid4

import asc_scrapper.schemas as asc_schemas
from app import crud, schemas
from app.db.init_db import InitializeDatabaseWithASC
from app.schemas.enums import CollageShifts


class InitializeDatabaseWithASCV2(InitializeDatabaseWithASC):
    def init_classes(self):
        computer_science_department = crud.department.create(
            db=self.db, obj_in=schemas.DepartmentCreate(
                name="علوم الحاسوب",
                en_name="Computer Science",
                abbr="CS",
                vision=None,
            )
        )
        branches = [
            schemas.Branch(
                id=uuid4(),
                name="برمجيات",
                en_name="Software",
                abbr="SW",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="نظم معلومات",
                en_name="Information Systems",
                abbr="IS",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="ذكاء اصطناعي",
                en_name="Artificial Intelligence",
                abbr="AI",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="أمنية حاسوب",
                en_name="Computer Security",
                abbr="CS",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="إدارة شبكات",
                en_name="Networks",
                abbr="NW",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="وسائط متعددة",
                en_name="Multimedia",
                abbr="MM",
                vision=None,
                department_id=computer_science_department.id
            ),
        ]
        for branch in branches:
            crud.branch.create(
                db=self.db, obj_in=branch
            )

        other = crud.branch.create(
            db=self.db, obj_in=schemas.BranchCreate(
                id=uuid4(),
                name="اخرى",
                en_name="",
                abbr="MM",
                vision=None,
                department_id=computer_science_department.id
            ),
        )

        levels: dict[str, int] = {
            "أول": 1,
            "ثاني": 2,
            "ثالث": 3,
            "رابع": 4,
        }
        shifts: dict[str, CollageShifts] = {
            "صباحي": CollageShifts.morning,
            "مسائي": CollageShifts.evening,
        }
        classes = self.asc.get_all(asc_schemas.Class)

        for class_ in classes:
            if class_.name not in ["", " "]:
                if len(class_.name.split()) < 3:
                    self.stages_ids[class_.id] = crud.stage.create(
                        db=self.db, obj_in=schemas.StageCreate(
                            name=class_.name,
                            shift=CollageShifts.morning,
                            level=None,
                            branch_id=other.id,
                        )
                    ).id
                else:
                    name = re.sub(' +', ' ', class_.name)

                    name = name.split()
                    level = levels[name[0]]
                    shift = shifts[name[-1]]
                    branch: schemas.Branch = list(filter(lambda b: b.name == branch, branches))[0]

                    self.stages_ids[class_.id] = crud.stage.create(
                        db=self.db, obj_in=schemas.StageCreate(
                            shift=shift,
                            level=level,
                            branch_id=branch.id,
                        )
                    ).id
