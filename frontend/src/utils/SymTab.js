class SymTab {
    constructor() {
        this.scopes = [{}]
    }

    pushScope() {
        this.scopes.push({})
    }

    popScope() {
        this.scopes.pop()
    }

    declareVar(name, value) {
        const currentScope = this.scopes[this.scopes.length - 1]
        currentScope[name] = value
    }

    updateVar(name, value) {
        for (let i = this.scopes.length - 1; i >= 0; i--) {
            if (name in this.scopes[i]) {
                this.scopes[i][name] = value
                return
            }
        }
        console.error(`Variable ${name} not defined`)
    }

    lookupVar(name) {
        for (let i = this.scopes.length - 1; i >= 0; i--) {
            if (name in this.scopes[i]) {
                return this.scopes[i][name]
            }
        }
        console.error(`Variable ${name} not defined`)
        return null
    }
}

export default SymTab
