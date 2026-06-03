<script lang="ts">
    import Topbar from './components/Topbar.svelte';
    import Sidebar from './components/Sidebar.svelte';
    import Textarea from './components/Textarea.svelte';
</script>

<main style="display: flex; flex-direction: row; flex: 1; height: 100%;">
    <Sidebar />
    <div style="display: flex; flex-direction: column; flex: 1;">
        <div style="width: auto; margin-left: auto;"><Topbar /></div>
        <Textarea />
    </div>
</main>