from app.models.address import Address
from app.dto.address import AddressDTO

def address_to_dto(address: Address) ->AddressDTO:
    return AddressDTO(
        id = address.id,
        country = address.country,
        city = address.city,
        street = address.street
    )

def dto_to_address(dto: AddressDTO) -> Address:
    return Address(
        id = dto.id,
        country = dto.country,
        city = dto.city,
        street = dto.street
    )
