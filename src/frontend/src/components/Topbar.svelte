<script lang="ts">
    import { onMount } from "svelte";
    import { getPyAPI } from "../utils/pywebview";

    let pyAPI: any = null;

    onMount(async () => {
        pyAPI = await getPyAPI();
    });
    
    const exitSymbol: string = "✖"
    const maximizeSymbol: string = "□"
    const minimizeSymbol: string = "━"

    async function minimize() { await pyAPI?.minimizeApp() }
    async function maximize() { await pyAPI?.maximizeApp() }
    async function exit() { await pyAPI?.exitApp() }
</script>

<main>
    <button class="other" on:click={() => minimize()}>{minimizeSymbol}</button>
    <button class="other" on:click={() => maximize()}>{maximizeSymbol}</button>
    <button class="exit" on:click={() => exit()}>{exitSymbol}</button>
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
