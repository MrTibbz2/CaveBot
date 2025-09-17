// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { getExpressionById } from './desmos'
import { api } from './api'

let calculatorInstance = null

export const bot = {
  pos: { x: 0, y: 0 },
  angle: 0,
  sensors: {
    leftfront: { x: -10, y: 5, angle: 270},
    leftback: { x: -10, y: -5, angle: 270},
    rightfront: { x: 10, y: 5, angle: 90},
    rightback: { x: 10, y: -5, angle: 90},
    frontleft: { x: -5, y: 10, angle: 0},
    frontright: { x: 5, y: 10, angle: 0},
    backleft: { x: -5, y: -10, angle: 180},
    backright: { x: 5, y: -10, angle: 180}
  },

  setCalculator(calculator) {
    console.log('Setting calculator instance:', calculator ? 'SUCCESS' : 'NULL')
    calculatorInstance = calculator
    if (calculator) {
      console.log('Calculator expressions available:', calculator.getExpressions().length)
    }
  },

  async move(distance) {
    console.log('Bot moving:', distance, 'at angle:', this.angle)
    const response = await fetch(`/pointcalc?angle=${this.angle}&distance=${distance}`)
    const offset = await response.json()
    
    this.pos.x += offset.x_pos
    this.pos.y += offset.y_pos
    console.log('New bot position:', this.pos)
    
    // Store position in backend
    await api.updateBotPosition(this.pos.x, this.pos.y, this.angle)
    
    if (calculatorInstance) {
      const xExpr = getExpressionById(calculatorInstance, "X_Position")
      const yExpr = getExpressionById(calculatorInstance, "Y_Position")
      
      if (xExpr && yExpr) {
        xExpr.latex = `N=${this.pos.x}`
        yExpr.latex = `M=${this.pos.y}`
        
        calculatorInstance.setExpression(xExpr)
        calculatorInstance.setExpression(yExpr)
      }
    }
  },

  async rotate(degrees) {
    this.angle += degrees
    if (this.angle >= 360) this.angle -= 360
    if (this.angle < 0) this.angle += 360
    console.log('Bot rotated to angle:', this.angle)
    
    // Store position in backend
    await api.updateBotPosition(this.pos.x, this.pos.y, this.angle)
    
    if (calculatorInstance) {
      const angleExpr = getExpressionById(calculatorInstance, "Angle")
      if (angleExpr) {
        angleExpr.latex = `R=${this.angle}`
        calculatorInstance.setExpression(angleExpr)
      }
    }
  }
}

let pointCounter = 0

export async function plotPoint(point, sensor = 'unknown') {
  console.log('Attempting to plot point:', point)
  
  // Store point in backend
  await api.addMapPoint(point.x, point.y, sensor)
  
  if (!calculatorInstance) {
    console.error('No calculator instance available for plotting')
    return
  }
  
  const pointExpr = {
    id: `plotted_point${pointCounter++}`,
    type: 'expression',
    latex: `(${point.x}, ${point.y})`,
    color: '#388c46',
    pointSize: "12",
  }
  
  console.log('Plotting point expression:', pointExpr)
  calculatorInstance.setExpression(pointExpr)
  console.log('Point plotted successfully')
}