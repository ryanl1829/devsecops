import highlightLines from 'markdown-it-highlight-lines'

export default {
  engine: ({marp}) => marp.use(highlightLines),
}
