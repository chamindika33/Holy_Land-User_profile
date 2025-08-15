from pydantic import BaseModel


class AdminApproveRequest(BaseModel):
    user_id: str
    admin_status: str

class AllUserData(BaseModel):
    page_number : int
    record_per_page : int

