<script lang="ts">
    import Topbar from "./components/Topbar.svelte";
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
</script>

<main>
    <Sidebar onSelect={handleSelect} />
    <div class="content">
        <div class="topbar"><Topbar /></div>
        <Textarea fileName={selectedFile} />
    </div>
</main>

<style>
    main {
        display: flex;
        flex: 1;
        height: 100%;
    }

    .content {
        display: flex;
        flex-direction: column;
        flex: 1;
    }

    .topbar {
        width: auto;
    }
</style>
