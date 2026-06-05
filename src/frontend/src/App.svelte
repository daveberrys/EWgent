<script lang="ts">
    import Sidebar from "./components/Sidebar.svelte";
    import Textarea from "./components/Textarea.svelte";
    import { getPyAPI } from "./utils/pywebview";
    import { onMount } from "svelte";
    
    let pyAPI: any = $state(null);
    onMount(async () => {
        pyAPI = await getPyAPI();
        pyAPI.appInit();
    });
    
    let selectedFile: string | null = $state(null);

    function handleSelect(name: string) {
        selectedFile = name;
    }

    function handleDelete(name: string) {
        if (selectedFile === name) {
            selectedFile = null;
        }
    }
</script>

<div class="appContainer">
    <main>
        <Sidebar onSelect={handleSelect} onDelete={handleDelete} />
        <section class="content">
            <Textarea fileName={selectedFile} />
        </section>
    </main>
</div>

<style>
    .appContainer {
        display: flex;
        flex-direction: column;
        height: 100vh;
        width: 100vw;
        background-color: var(--bg-primary);

        main {
            display: flex;
            flex: 1;
            overflow: hidden;

            .content {
                display: flex;
                flex-direction: column;
                flex: 1;
                background-color: var(--bg-primary);
            }
        }
    }
</style>
