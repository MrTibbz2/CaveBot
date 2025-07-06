import { expressions } from './expressions'

export function initializeDesmos(container) {
  console.log('Initializing Desmos calculator')
  const calculator = window.Desmos.GraphingCalculator(container, {
    keypad: false,
    expressions: false,
    settingsMenu: false,
  })

  console.log('Adding expressions to calculator:', expressions.length)
  // Add all expressions
  expressions.forEach((expr, index) => {
    console.log(`Adding expression ${index + 1}/${expressions.length}: ${expr.id}`)
    calculator.setExpression(expr)
  })

  console.log('Desmos calculator initialized')
  return calculator
}

export function getExpressionById(calculator, id) {
  const expressions = calculator.getExpressions()
  const found = expressions.find(expr => expr.id === id)
  console.log(`Looking for expression '${id}':`, found ? 'FOUND' : 'NOT FOUND')
  if (!found) {
    console.log('Available expressions:', expressions.map(e => e.id))
  }
  return found
}