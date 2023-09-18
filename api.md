common headers:

```
{
  Content-Type: application/json,
  Authorization: Token <token>
}
```

# Farms

## endpoint: `/farms/farms/`

get list of all farms assigned to logged in user

farm object:

```
{
    "id": int,
    "is_active": bool,
    "created": DateTime (ISOString),
    "updated": DateTime (ISOString),
    "name": string,
    "frp_port": int,
    "type": int,
    "no_of_domes": int,
    "no_of_growing_lines": int,
    "no_of_irrigation_tanks": int,
    "no_of_cooling_tanks": int,
    "no_of_ro_tanks": int,
    "no_of_rw_tanks": int,
    "inverter_power_output": float",
    "inverter_phasing": int,
    "battery_capacity": int,
    "solar_power_output": float,
    "area": float,
    "length": float,
    "width": "float,
    "latitude": int,
    "longitude": int,
    "direction": int,
    "iotbox": {
      <iotbox-details>
    }
```

method: GET

Response:

```
[
  { farm-object-1 },
  { farm-object-2 },
  { farm-object-3 },
  ...
]
```

## endpoint: `/farms/upload-image/`

upload an image

method: POST

Request body:

```
{
  "file": "file-object"
}
```

Response:

```
{
  "filename": "filename of the file",
  "url": "url of file in s3 bucket"
}
```

# User management

## endpoint: `/users/login/`

login an existing user

request body:

```
{
  "username": "username",
  "password": "password"
}
```

response:

- success:
  ```
  {
    "token": "token",
    "user_id": "user id",
    "username": "username"
  }
  ```

## endpoint: `/users/labours/`

get list of all labours

labour object:

```
{
    "id": int,
    "name": string,
    "mobile": int,
    "photo": url,
    "aadhar_int": int,
    "aadhar_front": url,
    "aadhar_back": url,
    "is_active": true,
    "created": dateTime (iso String),
    "updated": dateTime (iso String),
    "farms": [ // List of farm ids (farms assigned to the labour)
      1,
      2
    ]
}
```

method: GET

Response:

```
[
  { labour-object-1 },
  { labour-object-2 },
  { labour-object-3 },
  ...
]
```

## endpoint: `/users/labours/`

method: POST

register a labour

request body:

```
{
    "id": int,
    "name": string,
    "mobile": int,
    "photo": url,
    "aadhar_int": int,
    "aadhar_front": url,
    "aadhar_back": url,
    "is_active": true,
    "created": dateTime (iso String),
    "updated": dateTime (iso String),
    "farms": [ // List of farm ids  to assign to the labour
      1,
      2
    ]
}
```

Response:

```
{
  newly created labour object
}
```

## endpoint: `/users/labours?farm=<id>`

get list of all labours assigned to farm id

labour object:

```
{
    "id": int,
    "name": string,
    "mobile": int,
    "photo": url,
    "aadhar_int": int,
    "aadhar_front": url,
    "aadhar_back": url,
    "is_active": true,
    "created": dateTime (iso String),
    "updated": dateTime (iso String),
    "farms": [ // List of farm ids (farms assigned to the labour)
      1,
      2
    ]
}
```

method: GET

Response:

```
[
  { labour-object-1 },
  { labour-object-2 },
  { labour-object-3 },
  ...
]
```

## endpoint: `/users/labours/<id>/`

get labour with id \<id\>

labour object:

```
{
    "id": int,
    "name": string,
    "mobile": int,
    "photo": url,
    "aadhar_int": int,
    "aadhar_front": url,
    "aadhar_back": url,
    "is_active": true,
    "created": dateTime (iso String),
    "updated": dateTime (iso String),
    "farms": [ // List of farm ids (farms assigned to the labour)
      1,
      2
    ]
}
```

method: GET

query params:
id: farm-id for which labour list is required

Response:

```
{
    "id": int,
    "name": string,
    "mobile": int,
    "photo": url,
    "aadhar_int": int,
    "aadhar_front": url,
    "aadhar_back": url,
    "is_active": true,
    "created": dateTime (iso String),
    "updated": dateTime (iso String),
    "farms": [ // List of farm ids (farms assigned to the labour)
      1,
      2
    ]
}
```

# PDC

## endpoint: `/pdc/labour/work/`

method: POST

request body:

```
{
  datetime: datetime
  farm: id
  labour: id
  duration: int
  user: id
  description: string
  type: int
  work_quantity: int
  recipe: int
  recipe_quantity: int
  water_quantity: int
  dome: int
  remarks: string
}
```

response codes:

- success: 200

## endpoint: `/pdc/labour/attendance/`

method: POST

request body:

```
{
  labour: id
  datetime: datetime
  action: 0 (Punch in), 1 (Punch Out)
}
```

response codes:

- success: 200

## endpoint: `/pdc/user/attendance/`

method: POST

request body:

```
{
  user: id
  datetime: datetime
  action: 0 (Punch in), 1 (Punch Out)
}
```

response codes:

- success: 200

## endpoint: `/pdc/specimen/health/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  specimen: id
  germination: float
  plant_height: float
  nodes: int
  remarks: int (dropdown)
  observation: int (dropdown)
}
```

response codes:

- success: 200

## endpoint: `/pdc/specimen/growth/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  specimen: id
  plant_height: float
  stem_diameter: float
  internode_distance: float (optional)
  nodes: int (optional)
  no_of_branches: int
  no_of_branch_nodes  : int
  fruit_distance: float,
  no_of_petioles: float,
  length_of_petioles: float,
  leaves_in_petioles: float,
}
```

response codes:

- success: 200

## endpoint: `/pdc/specimen/flowering/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  specimen: id
  cluster: int
  flowering: {
    data: [
      {
        cluster: int,
        female_flowers: int,
        fruits: int
      }
    ]
  }
}
```

response codes:

- success: 200

## endpoint: `/pdc/specimen/output/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  specimen: id
  harvested_fruits: int
  harvested_weight: int
  stage_of_harvest: char
}
```

response codes:

- success: 200

## endpoint: `/pdc/dome/pollination/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  line: int
  section: choice (a, b, c)
  morning: float
  evening: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/dome/harvesting/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  line: int
  section: choice (a, b, c)
  total_weight: float
  pure_weight: float
  wastage_weight: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/plant-analysis/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  batch: str
  no_of_fruits: int
  weight_of_fruits: float
  brix_value: float
  fruit_color: str
}
```

response codes:

- success: 200

## endpoint: `/pdc/dome/root-weight/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  line: int
  section: choice (a, b, c)
  type: choice (dry, wet)
  weight: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/dome/leaf-temperature/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  line: int
  section: (a, b, c)
  temperature: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/dome/root-zone-temperature/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  line: int
  section: choice (a, b, c)
  water_temp: float
  surface_temp: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/climate/outside/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  weather: string
  wind_speed: float
  wind_direction: float
  temp: float
  humidity: float
  light: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/climate/dome/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  temp: float
  dry_temp: float
  wet_temp: float
  humidity: float
  light: float
  par_meter: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/exhaust/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  type: choice (ex, ve, co, sh)
  device_int: int
  status: int
}
```

response codes:

- success: 200

## endpoint: `/pdc/irrigation/outer/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  type: choice (ro, rw)
  ec: float
  ph: float
  do: float
  temp: float
  lph: float
  media_filter: float
  pressure: float
}
```

response codes:

- success: 200

## endpoint: `/pdc/irrigation/inner/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  dome: int
  recipe_name: int
  ph: float
  ec: float
  do: float
  nutrition_stage: choice
  temp: float
  water_quantity: float
  remarks: choice
  remarks_quantity: int
}
```

response codes:

- success: 200

## endpoint: `/pdc/irrigation/cooling-pad/`

method: POST

request body:

```
{
  farm: id
  datetime: datetime
  ph: float
  ec: float
  tank_temp: float
  remarks: int
}
```

response codes:

- success: 200
