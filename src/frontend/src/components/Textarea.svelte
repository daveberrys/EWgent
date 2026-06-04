<script lang="ts">
    import { onMount } from "svelte";
    import { getPyAPI } from "../utils/pywebview";

    let { fileName }: { fileName: string | null } = $props();

    let pyAPI: any = $state(null);
    let content: string = $state("");
    let saveTimer: ReturnType<typeof setTimeout> | null = $state(null);

    onMount(async () => {
        pyAPI = await getPyAPI();
    });

    async function loadContent(name: string) {
        content = await pyAPI.getFileContent(name);
    }

    function scheduleSave() {
        if (saveTimer) clearTimeout(saveTimer);
        saveTimer = setTimeout(async () => {
            if (fileName) {
                await pyAPI.saveFile(fileName, content);
            }
        }, 100);
    }

    $effect(() => {
        if (fileName && pyAPI) {
            loadContent(fileName);
        } else if (!fileName) {
            content = "";
        }
    });
</script>

<main>
    {#if fileName}
        <textarea bind:value={content} oninput={scheduleSave} placeholder="Type something here!"></textarea>
    {:else}
        <div class="empty">
            <p>Select a file to start editing</p>
        </div>
    {/if}
</main>

<style>
    main {
        display: flex;
        flex: 1;
        min-height: 0;
    }

    textarea {
        background-color: var(--background);
        color: white;
        flex: 1;
        border: none;
        outline: none;
        resize: none;
        padding: 10px;
        font-family: inherit;
        font-size: inherit;
    }

    .empty {
        display: flex;
        flex: 1;
        align-items: center;
        justify-content: center;
        color: #888;
    }
</style>
