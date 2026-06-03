<script lang="ts">
    import { onMount } from "svelte";
    import { getPyAPI } from "../utils/pywebview";

    let { onSelect }: { onSelect?: (name: string) => void } = $props();

    let pyAPI: any = $state(null);
    let files: string[] = $state([]);

    onMount(async () => {
        pyAPI = await getPyAPI();
        files = await pyAPI.getFiles();
    });

    async function selectFile(file: string) {
        onSelect?.(file);
    }

    async function createFile() {
        const name = prompt("Enter file name:");
        if (name && name.trim()) {
            await pyAPI.saveFile(name.trim(), "");
            files = await pyAPI.getFiles();
        }
    }

    async function deleteFile(file: string) {
        const confirmed = window.confirm(
            `Are you sure you want to permanently delete "${file}"?`,
        );
        if (confirmed) {
            await pyAPI.deleteFile(file);
            files = await pyAPI.getFiles();
        }
    }
</script>

<main>
    {#each files as file}
        <div class="filesButton">
            <button class="open" onclick={() => selectFile(file)}>
                <span>{file}</span>
            </button>
            <button class="delete" onclick={() => deleteFile(file)}>
                <b>x</b>
            </button>
        </div>
    {/each}
    <button class="add" onclick={() => createFile()}>
        <b>+</b>
    </button>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        resize: horizontal;
        min-width: 200px;
        max-width: 400px;
        padding: 10px;
        gap: 5px;
    }

    button {
        border: none;
        color: var(--text);
        background-color: var(--card);
        padding: 10px 15px;
        transition: all 0.1s ease-out;
        border-radius: 5px;
        text-align: left;
    }

    button:hover {
        filter: brightness(120%);
    }

    .filesButton {
        display: flex;
        min-width: 200px;
        max-width: 400px;
        gap: 5px;
    }

    .open {
        flex: 1;
    }

    .delete:hover {
        background-color: var(--exit);
    }

    .add {
        text-align: center;
    }
</style>
