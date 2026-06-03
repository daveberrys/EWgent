<script lang="ts">
    let text = "";
</script>

<main>
    <textarea bind:value={text} placeholder="Type something here!"></textarea>
</main>

<style>
    main {
        display: flex;
        flex: 1;
        min-height: 0;
        
        textarea {
            background-color: var(--background);
            color: white;
            
            flex: 1;
            border: none;
            outline: none;
            resize: none;
        }
    }
</style>