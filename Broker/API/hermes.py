from pydantic import BaseModel, ValidationError


class message(BaseModel):
    requestType: str
    packageSize: float
    connectionString: str
    signatory: str

    class signedPackage(BaseModel):
        oToken: str
        passPhrase: str


def CreateMessage():
    return "Hi"
