// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { bot, plotPoint } from './bot'

function toRadians(degrees) {
  return degrees * (Math.PI / 180)
}

function roundObjectNumbers(obj, decimals = 2) {
  if (typeof obj === 'number') {
    return Number(obj.toFixed(decimals))
  }
  if (Array.isArray(obj)) {
    return obj.map(v => roundObjectNumbers(v, decimals))
  }
  if (typeof obj === 'object' && obj !== null) {
    const result = {}
    for (const key in obj) {
      result[key] = roundObjectNumbers(obj[key], decimals)
    }
    return result
  }
  return obj
}

function GetSensorVector(sensor) {
  if (bot.sensors[sensor] == null) {
    console.error(`Sensor ${sensor} not found in bot measurements.`)
    return null
  }
  const sensorData = bot.sensors[sensor]
  // Rotate the sensor's offset by the bot's current angle (cartesian)
  const botAngleRad = toRadians(bot.angle || 0) // Use bot.angle if available, otherwise default to 0
  // Corrected rotation for clockwise angle (0=North)
  // Rotate the sensor's offset by the bot's current angle (clockwise)
  const rotatedX = sensorData.x * Math.cos(botAngleRad) + sensorData.y * Math.sin(botAngleRad)
  const rotatedY = -sensorData.x * Math.sin(botAngleRad) + sensorData.y * Math.cos(botAngleRad)
  // Normalize angle to [0, 360)
  let angle = (sensorData.angle + bot.angle) % 360
  if (angle < 0) angle += 360
  // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
  const sensorVec = {
    x: bot.pos.x + rotatedX,
    y: bot.pos.y + rotatedY,
    angle: angle
  }
  return roundObjectNumbers(sensorVec, 2)
}

async function CalcPoint(distance, sensor) {
  const sensorVector = GetSensorVector(sensor)
  if (!sensorVector || typeof sensorVector.angle !== 'number' || typeof sensorVector.x !== 'number' || typeof sensorVector.y !== 'number') {
    console.error('CalcPoint: Invalid sensorVector for', sensor, sensorVector)
    return { x: NaN, y: NaN }
  }
  const response = await fetch(`/pointcalc?angle=${sensorVector.angle}&distance=${distance}`)
  const offsets = await response.json()
  if (!offsets || typeof offsets.x_pos !== 'number' || typeof offsets.y_pos !== 'number' || isNaN(offsets.x_pos) || isNaN(offsets.y_pos)) {
    console.error('CalcPoint: Invalid offsets from vecmath.getPointCalc:', offsets)
    return { x: NaN, y: NaN }
  }
  // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
  const point = {
    x: sensorVector.x + offsets.x_pos,
    y: sensorVector.y + offsets.y_pos
  }
  return roundObjectNumbers(point, 2)
}

export async function addPoints(distanceReads) {
  console.log('Adding points from sensor data:', distanceReads.payload)
  for (let i = 0; i < Object.keys(bot.sensors).length; i++) {
    let sensor = Object.keys(bot.sensors)[i]
    let distance = distanceReads.payload[sensor]
    if (distance == null) { continue }
    else {
      // Calculate point based on sensor and distance
      console.log(`Processing sensor ${sensor} with distance ${distance}`)
      let point = await CalcPoint(distance, sensor)
      if (point.x !== NaN && point.y !== NaN) {
        console.log(`Plotting point for ${sensor}:`, point)
        plotPoint(point)
      } else {
        console.error(`Invalid point for sensor ${sensor}:`, point)
      }
    }
  }
}