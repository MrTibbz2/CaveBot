#notes for keeping track of what I'm doing

what am I using?

- htmx probably cause I know it
- tailwind looks good
- web sockets using native js es6
- fastapi because easy (apparently)
- canvas for drawing
- yeah thats about it

```
pip install fastapi uvicorn jinja2    
```


how is websocket formatted
- js object/python dict


**Format:** 
```
{
    type: <messagetype in string>, 
    timestamp: "2025-06-22T12:34:56Z", // datetime
    subtype: <subtype, eg what kind of log> // optional
    payload: {
        <all stuff for the message>
    }

}
```

example:
```
{
    type: "log"
    subtype: "pico_info"
    timestamp: "2025-06-22T12:34:56Z",
    payload: {
        message: "hi from pico"
    }
}
{
    type: "data_stream"
    subtype: "distance_read" // could be botposition, botangle, etc. 
    timestamp: "2025-06-22T12:34:56Z",
    payload: {
        sensor_leftfront: 2.5 // in cm, float
        // other sensors
        // if sensor is a negative value like -1 then its invalid.
    }
}
```