import adapterStatic from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';

export default {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: preprocess(),

    kit: {
        adapter: adapterStatic({
            fallback: 'index.html',
        }),
        prerender: { entries: [] },
    },
};