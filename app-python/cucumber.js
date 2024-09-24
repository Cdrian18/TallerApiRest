module.exports = {
  default: `--import ./tests/features/step_definitions/*.mjs --format html:./reports/cucumber-report.html --format junit:./reports/junit_report.xml --format progress ./tests/features/*.feature`
};
