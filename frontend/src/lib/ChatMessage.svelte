<script>
	// Props for the ChatMessage component
	export let message = ''; // The text content of the message
	export let sender = 'user'; // 'user' or 'bot', determines styling and alignment
</script>

<div class="flex" class:justify-end={sender === 'user'} class:justify-start={sender === 'bot'}>
	{#if sender === 'bot'}
		<div class="w-10 h-10 ml-2 flex-shrink-0 bg-neutral-400 rounded-full mt-[14px]"></div>
	{/if}
	<div
		class="max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-2xl"
		class:text-white={sender === 'user'}
		class:bg-neutral-400={sender === 'user'}
		class:text-neutral-800={sender === 'bot'}
	>
		<p class="text-sm whitespace-pre-wrap">{message}</p>
	</div>
</div>
