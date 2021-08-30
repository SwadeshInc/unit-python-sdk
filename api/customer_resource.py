from api.base_resource import BaseResource
from models.customer import *
from models.codecs import DtoDecoder


class CustomerResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "customers"

    def update(self, request: Union[PatchIndividualCustomerRequest, PatchBusinessCustomerRequest]) -> Union[UnitResponse[CustomerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.customer_id}", payload)

        if response.ok:
            data = response.json().get("data")
            if data["type"] == "individualCustomer":
                return UnitResponse[IndividualCustomerDTO](DtoDecoder.decode(data), None)
            else:
                return UnitResponse[BusinessCustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())


    def get(self, customer_id: str) -> Union[UnitResponse[CustomerDTO], UnitError]:
        response = super().get(f"{self.resource}/{customer_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[CustomerDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
