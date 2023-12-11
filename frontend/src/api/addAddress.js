import { apiAddress } from '.'

//async def add_address(street_name, house_nr, apartament_nr, city, db: SessionLocal = Depends(get_db)):

export const addAddress = async (streetName, houseNr, apartamentNr, city) => {
    return await fetch(`${apiAddress}/addresses`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            street_name: streetName,
            house_nr: houseNr,
            apartament_nr: apartamentNr,
            city,
        }),
    }).then((res) => res.json())
}
