<script lang="ts">
    const exitSymbol: string = "✖"
    const maximizeSymbol: string = "□"
    const minimizeSymbol: string = "━"
</script>

<main>
    <button class="other" on:click={() => console.log({minimizeSymbol})}>{minimizeSymbol}</button>
    <button class="other" on:click={() => console.log({maximizeSymbol})}>{maximizeSymbol}</button>
    <button class="exit" on:click={() => console.log({exitSymbol})}>{exitSymbol}</button>
</main>

<style>
    main {
        display: flex;
        
        button {
            background: none;
            border: none;
            color: var(--color);
            width: 50px;
            padding: 5px;
            transition: background-color 0.1s ease-out;
    
            &:hover.exit {
                background-color: var(--exit);
            } &:hover.other {
                background-color: var(--misc);
            }
        }
    }
</style>