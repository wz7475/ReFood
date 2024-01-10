function deg2rad(deg) {
    return deg * (Math.PI / 180)
}

export const getDistanceFromLatLonInKm = (point1, point2) => {
    let R = 6371 // Radius of the earth in km
    let dLat = deg2rad(point2.latitude - point1.latitude)
    let dLon = deg2rad(point2.longitude - point1.longitude)
    let a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(point1.latitude)) *
            Math.cos(deg2rad(point2.latitude)) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2)
    let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
}
