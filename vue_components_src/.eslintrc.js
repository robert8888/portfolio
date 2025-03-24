module.exports = {
  root: true,
  env: {
    node: true,
    "es6": true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended',
    '@vue/typescript/recommended',
    '@vue/typescript'
  ],
  parserOptions: {
    ecmaVersion: 2020,
    parser: '@typescript-eslint/parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    "@typescript-eslint/ban-ts-ignore": "off",
    "prefer-const": "warn",
    "vue/valid-template-root": "off",
    "no-undef": "off",
    'vue/no-multiple-template-root': 'off',
    'vue/multi-word-component-names': 'off',
    'vue/no-reserved-props': 'off',
    'vue/no-unused-components': 'off',
    'vue/return-in-computed-property': 'off',
  }
}
