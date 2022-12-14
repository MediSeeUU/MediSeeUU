# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.db import models


class NotVarCharField(models.CharField):
    """
    Special field type that enforces CHAR instead of VARCHAR
    It derives from the Django CharField.
    """    
    def db_type(self, connection):
        """
        db_type returns the database field type for the given connection. 
        This function specifically returns CHAR instead of VARCHAR.

        Args:
            connection (_type_): Connection with the database.

        Returns:
            str: It returns the column data type for the given connection as string,
            but it will return 'char' if it would be a 'varchar'.
        """        
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char


class AutTypes(models.TextChoices):
    """
    Choice types for eu_aut_type. Is derived from the enumerated choice class.
    """    
    CONDITIONAL = "CONDITIONAL",
    EXCEPTIONAL = "EXCEPTIONAL",
    STANDARD = "STANDARD"
    UNCERTAIN = "EXCEPTIONAL OR CONDITIONAL"


class AutStatus(models.TextChoices):
    """
    Choice types for eu_aut_status. Is derived from the enumerated choice class.
    """   
    ACTIVE = "ACTIVE",
    WITHDRAWAL = "WITHDRAWN",
    REFUSALS = "REFUSED"


class LegalBasesTypes(models.TextChoices):
    """
    Choice types for legal bases. Is derived from the enumerated choice class.
    """
    article48 = "article 4.8",
    article4_8 = "article 4(8)"
    article48_1 = "article 4.8(1)",
    article48_2 = "article 4.8(2)",
    article48_3 = "article 4.8(3)",
    article83 = "article 8.3",
    article8_3 = "article 8(3)",
    article101 = "article 10.1",
    article10_1 = "article 10(1)",
    article102 = "article 10.2",
    article10_2 = "article 10(2)",
    article103 = "article 10.3",
    article10_3 = "article 10(3)",
    article104 = "article 10.4",
    article10_4 = "article 10(4)",
    article10a = "article 10a",
    article10_a = "article 10(a)",
    article10b = "article 10b",
    article10_b = "article 10(b)",
    article10c = "article 10c",
    article10_c = "article 10(c)"
