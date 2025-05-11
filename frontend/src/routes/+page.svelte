<script lang="ts">
	const sourceText =
		"Photosynthesis usually refers to oxygenic photosynthesis, a process that produces oxygen. Photosynthetic organisms store the chemical energy so produced within intracellular organic compounds (compounds containing carbon) like sugars, glycogen, cellulose and starches. To use this stored chemical energy, an organism's cells metabolize the organic compounds through cellular respiration. Photosynthesis plays a critical role in producing and maintaining the oxygen content of the Earth's atmosphere, and it supplies most of the biological energy necessary for complex life on Earth";

	const notes = [
		'Photosynthesis typically refers to oxygenic photosynthesis, a process that results in the production of oxygen',
		'Organisms that perform photosynthesis store the chemical energy they produce in intracellular organic compounds such as sugars, glycogen, cellulose, and starches',
		"To utilize this stored chemical energy, an organism's cells perform cellular respiration, metabolizing the organic compounds",
		"Photosynthesis is vital for producing and maintaining the oxygen levels in Earth's atmosphere",
		'This process supplies the majority of the biological energy required for complex life on our planet'
	];

	import ChatMessage from '$lib/ChatMessage.svelte'; // Assuming ChatMessage.svelte is in the same directory or adjust path
	import Info from '$lib/Info.svelte';
	import Popover from '$lib/Popover.svelte';
	import { GoogleGenAI } from '@google/genai';

	const ai = new GoogleGenAI({ apiKey: import.meta.env.VITE_GEMINI_API_KEY });

	async function getEmbedding(text: string) {
		return (
			await ai.models.embedContent({
				model: 'gemini-embedding-exp-03-07',
				contents: text
			})
		).embeddings![0].values!;
	}

	function distance(a: number[], b: number[]) {
		let sum = 0;
		for (let i = 0; i < a.length; i++) {
			sum += Math.abs(a[i] - b[i]);
		}
		return sum;
	}

	async function linkMissingInfo(missing: string[]) {
		const noteEmbeddings = await Promise.all(
			notes.map(async (text, i) => ({ i, text, embedding: await getEmbedding(text) }))
		);

		return await Promise.all(
			missing.map(async (text) => {
				const embedding = await getEmbedding(text);
				noteEmbeddings.sort(
					(a, b) => distance(a.embedding, embedding) - distance(b.embedding, embedding)
				);
				return noteEmbeddings[0].text;
			})
		);
	}

	const chat = ai.chats.create({
		model: 'gemini-2.0-flash',
		config: {
			systemInstruction:
				"You are a curious but thoughtful 12-year-old student. You're trying to understand new topics being explained to you by someone older. When something is unclear, ask follow-up questions like a real middle schooler would. If an explanation is vague, confusing, or uses big words, ask the person to explain it more simply or give an example. You don't pretend to understand things you don't — instead, you react naturally, just like a real student trying to learn. Keep your responses respectful, curious, and age-appropriate."
		}
	});

	// Reactive state for the current input and messages
	let currentMessage = '';
	let messages: { id: number; text: string; sender: 'user' | 'bot' }[] = [];
	// let messages: { id: number; text: string; sender: 'user' | 'bot' }[] = [
	// 	{
	// 		id: 1,
	// 		text: "Okay, so imagine photosynthesis. Plants take sunlight, carbon dioxide, and water, and they convert it into glucose - that is a type of sugar - and oxygen. It's how they make their food.",
	// 		sender: 'user'
	// 	},
	// 	{
	// 		id: 2,
	// 		text: "Okay, I think I got it now! Sunlight, air stuff, and water turn into plant food and the air we breathe? That's pretty neat! So, the glucose is like their energy source?",
	// 		sender: 'bot'
	// 	},
	// 	{
	// 		id: 3,
	// 		text: "But you mentioned some 'carbon dioxide.' Where exactly do the plants get that from? Like, is it just... everywhere in the air? ☀️ →",
	// 		sender: 'bot'
	// 	},
	// 	{
	// 		id: 4,
	// 		text: "That's a great question! Yes, carbon dioxide (CO₂) is a gas that's naturally present in the Earth's atmosphere. Plants absorb it through tiny pores on their leaves called stomata. Think of them as little mouths that open and close to take in CO₂.",
	// 		sender: 'user'
	// 	}
	// ];

	let evaluation: {
		correct: string[];
		missing: { text: string; note: string | null }[];
		shortSentence: string;
	} | null = null;

	// let evaluation: {
	// 	correct: string[];
	// 	missing: string[];
	// 	shortSentence: string;
	// } | null = {
	// 	correct: ['You mentioned that', 'and this', 'and some of that'],
	// 	missing: [
	// 		'You forgot to mention this and some long text to make this dummy data wrap lines damn thats not enough lets add more text',
	// 		'and this',
	// 		'and some of that',
	// 		'You forgot to mention this',
	// 		'and this',
	// 		'and some of that',
	// 		'You forgot to mention this',
	// 		'and this',
	// 		'and some of that'
	// 	],
	// 	shortSentence: 'You have a good grasp of the basics of photosynthesis!'
	// };

	// Function to handle sending a message
	async function sendMessage() {
		if (currentMessage.trim() === '') {
			// ai.models.embedContent({
			//     model: 'gemini-embedding-exp-03-07',
			//     contents: ""
			// })

			let conversationStr = '';
			chat.getHistory().forEach((message) => {
				conversationStr += message.role! + ':\n' + message.parts![0]!.text! + '\n\n';
			});

			const grade = await ai.models.generateContent({
				config: {
					systemInstruction:
						'You will grade a students (user) knowledge retention based on a source text they studied from and a conversation where they tried to explain what they learned to a listener (model). You will first receive the source text and then the conversation. Provide a short sentence telling the student how he did and list the things they got right and what they missed from the source text.',
					responseMimeType: 'application/json',
					responseSchema: {
						type: 'OBJECT',
						properties: {
							shortSentence: {
								type: 'STRING'
							},
							correct: {
								type: 'ARRAY',
								items: {
									type: 'STRING'
								}
							},
							missing: {
								type: 'ARRAY',
								items: {
									type: 'STRING'
								}
							}
						},
						propertyOrdering: ['shortSentence', 'correct', 'missing']
					}
				},
				model: 'gemini-2.0-flash',
				contents: sourceText + '\nConversation:\n' + conversationStr
			});

			const { correct, missing, shortSentence } = JSON.parse(
				grade.candidates![0]!.content!.parts![0]!.text!
			);

			const linkedMissing = await linkMissingInfo(missing);

			evaluation = {
				correct,
				missing: missing.map((text, i) => ({ text, note: linkedMissing[i] })),
				shortSentence
			};

			return;
		}

		// Add the new user message to the messages array
		messages = [
			...messages, // Ensure previous bot messages don't show suggestion
			{
				id: messages.length + 1,
				text: currentMessage.trim(),
				sender: 'user'
			}
		];

		const res = await chat.sendMessage({
			message: currentMessage.trim()
		});

		currentMessage = ''; // Clear the input field

		// Simulate a bot response (you'd replace this with actual bot logic)
		messages = [
			...messages,
			{
				id: messages.length + 1,
				text: res.text!,
				sender: 'bot'
			}
		];
	}

	// Function to handle Enter key press in the input field
	function handleKeydown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault(); // Prevent new line on Enter
			sendMessage();
		}
	}
</script>

<div class="flex flex-col h-screen bg-gray-100 font-sans">
	<header class="p-4 flex items-center bg-gray-100 justify-between sticky top-0 z-10">
		<div class="flex items-center">
			<button class="text-gray-600 hover:text-gray-800 mr-3 lg:hidden">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-6 h-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
					/>
				</svg>
			</button>
			<h1 class="text-xl font-semibold text-gray-800">Your Highschool Friend</h1>
		</div>
		<button class="text-gray-600 hover:text-gray-800">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="w-6 h-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"
				/>
			</svg>
		</button>
	</header>

	<div class="flex flex-col overflow-y-auto flex-grow">
		<main class="flex flex-col flex-1 p-6 gap-4">
			{#each messages as msg (msg.id)}
				<ChatMessage message={msg.text} sender={msg.sender} />
			{/each}
		</main>

		{#if evaluation}
			<div class="min-h-[2px] bg-neutral-600 mx-8 self-stretch"></div>
			<div class="flex flex-col justify-center mx-10">
				<div class="flex flex-col self-center">
					<p class="text-xl mt-4">
						{evaluation.shortSentence}
					</p>
					<h1 class="text-xl mt-4 mb-2">You correctly explained the following concepts:</h1>
					{#each evaluation.correct as correct}
						<Info text={correct} />
					{/each}
					<h1 class="text-xl mt-4 mb-2">What wasn't quite clear in the explanation:</h1>
					{#each evaluation.missing as missing}
						<Info text={missing.text} note={missing.note} />
					{/each}
				</div>
			</div>
		{/if}
	</div>

	<footer class=" p-4 sticky bottom-0 z-10">
		<p class="text-xs text-center text-gray-500 mt-2 mb-1">
			Answer the question or find the answer
		</p>
		<div class="flex items-center max-w-3xl mx-auto">
			<textarea
				bind:value={currentMessage}
				on:keydown={handleKeydown}
				rows="1"
				class="flex-grow p-3 border bg-neutral-400 text-white placeholder-white rounded-full focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none overflow-y-auto max-h-24 mr-3"
				placeholder="Type here ..."
			></textarea>
			<button
				on:click={sendMessage}
				class="p-3 bg-indigo-500 text-white rounded-full hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors"
				aria-label="Send message"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-6 h-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15c.621 0 1.125-.504 1.125-1.125V6.375c0-.621-.504-1.125-1.125-1.125S10.875 5.754 10.875 6.375v7.5c0 .621.504 1.125 1.125 1.125z"
					/>
				</svg>
			</button>
		</div>
	</footer>
</div>

<style>
	/* For Tailwind JIT to pick up these classes if not directly used in <template> */
	/* bg-blue-500 text-white rounded-lg shadow rounded-bl-none */
	/* bg-gray-200 text-gray-800 rounded-lg shadow rounded-br-none */

	/* Custom scrollbar for message list (optional, for better aesthetics) */
	main::-webkit-scrollbar {
		width: 8px;
	}
	main::-webkit-scrollbar-thumb {
		background-color: #cbd5e1; /* gray-300 */
		border-radius: 4px;
	}
	main::-webkit-scrollbar-track {
		background-color: #f1f5f9; /* gray-100 */
	}

	/* Style for the textarea to grow with content up to a max-height */
	textarea {
		scrollbar-width: thin; /* For Firefox */
		scrollbar-color: #cbd5e1 #f1f5f9; /* For Firefox */
	}
	textarea::-webkit-scrollbar {
		width: 6px;
	}
	textarea::-webkit-scrollbar-thumb {
		background-color: #cbd5e1;
		border-radius: 3px;
	}
</style>
