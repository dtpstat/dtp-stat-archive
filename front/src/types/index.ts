enum ParticipantType {
    auto = "auto",
    bicycle = "bicycle",
    pedestrian = "pedestrian"
}

export type FilterType = {
    id: Number,
    type: String,
    param: String,
    value: String | Number,
    applied: Boolean,
    handleChange: Function
}

export type MVC = {
    id: Number,
    lat: Number,
    lng: Number,
    datetime: DeviceRotationRate,
    participant_type: ParticipantType
}

export type StateType = {
    filters: FilterType[] | null,
    mvcs: MVC[] | null
}

export type BriefType = {
    dead: Number,
    deadAuto: Number,
    deadBicycle: Number,
    deadPedestrian: Number,
    injured: Number,
    injuredAuto: Number,
    injuredBicycle: Number,
    injuredPedestrian: Number,
    mvcCount: Number
}