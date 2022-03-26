from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self,
                    name,
                    user_name,
                    position,
                    employment_date,
                    monthly_salary=0,
                    api_user=False,
                    paid_salary=0,
                    password=None,
                    ):

        if not name:
            raise ValueError('Пользователь должен иметь имя!')
        if not user_name:
            raise ValueError('Пользователь должен user_name!')

        user = self.model(
            name=name,
            password=password,
            user_name=user_name,
            position=position,
            employment_date=employment_date,
            monthly_salary=monthly_salary,
            paid_salary=paid_salary,
            api_user=api_user,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         name,
                         user_name,
                         position,
                         employment_date,
                         monthly_salary=0,
                         api_user=True,
                         paid_salary=0,
                         password=None,
                         ):
        user = self.create_user(
            name=name,
            user_name=user_name,
            password=password,
            position=position,
            employment_date=employment_date,
            monthly_salary=monthly_salary,
            paid_salary=paid_salary,
            api_user=api_user,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
