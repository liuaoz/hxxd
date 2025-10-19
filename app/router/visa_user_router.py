from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from core.response import JsonRet
from service.visa_user_service import VisaUserService

visa_user_router = APIRouter()


class AddRequest(BaseModel):
    lastName: str
    firstName: str
    province: str
    idNumber: str
    passport: str
    address: str
    phone: str
    email: str
    gender: str
    issueDate: str
    expirationDate: str
    birthDate: str

    def to_db_dict(self):
        return {
            "last_name": self.lastName,
            "first_name": self.firstName,
            "province": self.province,
            "id_number": self.idNumber,
            "passport": self.passport,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "gender": self.gender,
            "issue_date": self.issueDate,
            "expiration_date": self.expirationDate,
            "birth_date": self.birthDate,
        }

    @classmethod
    def from_db(cls, visa_user):
        def date_to_str(date_obj):
            if isinstance(date_obj, date):
                return date_obj.isoformat()  # 或者使用 str(date_obj)
            return date_obj

        return cls(
            lastName=visa_user.last_name,
            firstName=visa_user.first_name,
            province=visa_user.province,
            idNumber=visa_user.id_number,
            passport=visa_user.passport,
            address=visa_user.address,
            phone=visa_user.phone,
            email=visa_user.email,
            gender=visa_user.gender,
            issueDate=date_to_str(visa_user.issue_date),
            expirationDate=date_to_str(visa_user.expiration_date),
            birthDate=date_to_str(visa_user.birth_date)
        )

@visa_user_router.post("/create")
async def create_visa_user(request: AddRequest):
    visa_user = request.to_db_dict()

    await VisaUserService.add(visa_user)
    return JsonRet(message="签证用户添加成功")

@visa_user_router.get("/list")
async def list_visa_users():
    # 这里可以添加分页和过滤逻辑
    visa_users = await VisaUserService.list_all()
    visa_user_list = [AddRequest.from_db(user) for user in visa_users]
    return JsonRet(data=visa_user_list)