import scenarioScore from '../data/scenarioScore.json'

export function calculateScore(selectedScenario, weights) {
  let normalizedScore = 0
  if (Object.entries(weights).length !== 0 && weights.constructor === Object) {
    let { env, eco, soc } = scenarioScore.filter(
      scenario => scenario.scenario === selectedScenario
    )[0]
    normalizedScore = Math.round(
      (100 * (env * weights.env + eco * weights.eco + soc * weights.soc)) /
        findMaxScore(weights)
    )
    //console.log('selected scenario: ', selectedScenario)
  }
  if (isNaN(normalizedScore)) normalizedScore = 0
  return normalizedScore
}

const findMaxScore = weights => {
  let maxScore = -1
  //let bestScenario = 'none'
  if (Object.entries(weights).length !== 0 && weights.constructor === Object) {
    //For each possible scenario
    for (var t = 0; t <=1; t++) {
      for (var e = 0; e <= 26; e++) {
        for (var c = 0; c <= 7; c++) {
          for (var b = 0; b <= 3; b++) {
            const checkScenario = 'T' + t + 'E' + e + 'C' + c + 'B' + b
            let { env, eco, soc } = scenarioScore.filter(
              scenario => scenario.scenario === checkScenario
            )[0]
            let score = env * weights.env + eco * weights.eco + soc * weights.soc
            if (score > maxScore) {
              maxScore = score
              //bestScenario = checkScenario
            }
          }
        }
      }
    }
  }
  if (maxScore === 0) maxScore = -1
  //console.log('best scenario: ', bestScenario)
  return maxScore
}
