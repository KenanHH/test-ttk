// Quiz Application for Exam Preparation
(function() {
    'use strict';

    // Required areas - at least one question from each
    const REQUIRED_OBLASTI = [
        'Krivični zakon FBiH',
        'Zakon o kantonalnom tužilaštvu TK',
        'Zakon o krivičnom postupku FBiH',
        'Pravilnik o TCMS-u',
        'Zakon o državnoj službi TK'
    ];

    const QUESTIONS_PER_TEST = 10;
    const HISTORY_KEY = 'quiz_question_history';
    const HISTORY_SIZE = 50; // Remember last 50 questions to avoid repetition

    // State
    let allQuestions = [];
    let currentQuestions = [];
    let currentQuestionIndex = 0;
    let userAnswers = [];

    // DOM Elements
    const startScreen = document.getElementById('start-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const resultsScreen = document.getElementById('results-screen');
    const startBtn = document.getElementById('start-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const restartBtn = document.getElementById('restart-btn');
    const questionNumber = document.getElementById('question-number');
    const questionOblast = document.getElementById('question-oblast');
    const questionText = document.getElementById('question-text');
    const answersContainer = document.getElementById('answers');
    const progressBar = document.getElementById('progress');

    // Initialize
    async function init() {
        try {
            await loadQuestions();
            bindEvents();
        } catch (error) {
            console.error('Failed to initialize quiz:', error);
            alert('Greška pri učitavanju pitanja. Molimo osvježite stranicu.');
        }
    }

    // Load questions from JSON
    async function loadQuestions() {
        const response = await fetch('questions-answers.json');
        if (!response.ok) {
            throw new Error('Failed to load questions');
        }
        allQuestions = await response.json();
        console.log(`Loaded ${allQuestions.length} questions`);
    }

    // Bind event listeners
    function bindEvents() {
        startBtn.addEventListener('click', startQuiz);
        prevBtn.addEventListener('click', goToPreviousQuestion);
        nextBtn.addEventListener('click', goToNextQuestion);
        submitBtn.addEventListener('click', submitQuiz);
        restartBtn.addEventListener('click', restartQuiz);
    }

    // Cryptographically secure random number generator
    function secureRandom() {
        const array = new Uint32Array(1);
        crypto.getRandomValues(array);
        return array[0] / (0xFFFFFFFF + 1);
    }

    // Secure random integer in range [0, max)
    function secureRandomInt(max) {
        return Math.floor(secureRandom() * max);
    }

    // Shuffle array using Fisher-Yates with crypto random
    function shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = secureRandomInt(i + 1);
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    // Get question history from localStorage
    function getQuestionHistory() {
        try {
            const history = localStorage.getItem(HISTORY_KEY);
            return history ? JSON.parse(history) : [];
        } catch (e) {
            return [];
        }
    }

    // Save question history to localStorage
    function saveQuestionHistory(indices) {
        try {
            let history = getQuestionHistory();
            history = [...indices, ...history].slice(0, HISTORY_SIZE);
            localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
        } catch (e) {
            console.warn('Could not save question history');
        }
    }

    // Create a unique hash for a question (for deduplication)
    function getQuestionHash(question) {
        return `${question.oblast}:${question.pitanje.substring(0, 50)}`;
    }

    // Select questions ensuring at least one from each required oblast
    // with improved randomization and history tracking
    function selectQuestions() {
        const history = new Set(getQuestionHistory());
        const selected = [];
        const usedIndices = new Set();
        const usedHashes = new Set();

        // Prepare questions with metadata
        const questionsWithMeta = allQuestions.map((q, index) => ({
            ...q,
            originalIndex: index,
            hash: getQuestionHash(q),
            wasRecentlyUsed: history.has(index)
        }));

        // Shuffle the required oblasti order for variety
        const shuffledOblasti = shuffleArray(REQUIRED_OBLASTI);

        // First, pick one question from each required oblast
        // Prioritize questions that weren't recently used
        for (const oblast of shuffledOblasti) {
            const oblastQuestions = questionsWithMeta.filter(
                q => q.oblast === oblast &&
                     !usedIndices.has(q.originalIndex) &&
                     !usedHashes.has(q.hash)
            );

            if (oblastQuestions.length > 0) {
                // Separate into fresh and recently used
                const freshQuestions = oblastQuestions.filter(q => !q.wasRecentlyUsed);
                const recentQuestions = oblastQuestions.filter(q => q.wasRecentlyUsed);

                // Prefer fresh questions, but use recent if no fresh available
                const pool = freshQuestions.length > 0 ? freshQuestions : recentQuestions;

                // Shuffle and pick
                const shuffledPool = shuffleArray(pool);
                const selectedQuestion = shuffledPool[0];

                selected.push(selectedQuestion);
                usedIndices.add(selectedQuestion.originalIndex);
                usedHashes.add(selectedQuestion.hash);
            }
        }

        // Fill remaining slots with random questions from any oblast
        const remainingSlots = QUESTIONS_PER_TEST - selected.length;

        // Get available questions not yet selected
        const availableQuestions = questionsWithMeta.filter(
            q => !usedIndices.has(q.originalIndex) && !usedHashes.has(q.hash)
        );

        // Separate fresh and recent
        const freshAvailable = availableQuestions.filter(q => !q.wasRecentlyUsed);
        const recentAvailable = availableQuestions.filter(q => q.wasRecentlyUsed);

        // Heavily shuffle fresh questions multiple times for extra randomness
        let shuffledFresh = freshAvailable;
        for (let i = 0; i < 3; i++) {
            shuffledFresh = shuffleArray(shuffledFresh);
        }

        // Take from fresh first, then from recent if needed
        let added = 0;
        for (const q of shuffledFresh) {
            if (added >= remainingSlots) break;
            if (!usedHashes.has(q.hash)) {
                selected.push(q);
                usedIndices.add(q.originalIndex);
                usedHashes.add(q.hash);
                added++;
            }
        }

        // If still need more, use recent questions
        if (added < remainingSlots) {
            const shuffledRecent = shuffleArray(recentAvailable);
            for (const q of shuffledRecent) {
                if (added >= remainingSlots) break;
                if (!usedHashes.has(q.hash)) {
                    selected.push(q);
                    usedIndices.add(q.originalIndex);
                    usedHashes.add(q.hash);
                    added++;
                }
            }
        }

        // Save selected questions to history
        saveQuestionHistory(selected.map(q => q.originalIndex));

        // Triple shuffle the final selection for maximum randomness
        let finalSelection = selected;
        for (let i = 0; i < 3; i++) {
            finalSelection = shuffleArray(finalSelection);
        }

        // Add random answer order to each question
        return finalSelection.map(q => ({
            ...q,
            answerOrder: shuffleArray(['A', 'B', 'C'])
        }));
    }

    // Start the quiz
    function startQuiz() {
        currentQuestions = selectQuestions();
        currentQuestionIndex = 0;
        userAnswers = new Array(currentQuestions.length).fill(null);

        showScreen(quizScreen);
        displayQuestion();
    }

    // Display current question
    function displayQuestion() {
        const question = currentQuestions[currentQuestionIndex];

        // Update question number and oblast
        questionNumber.textContent = `Pitanje ${currentQuestionIndex + 1} od ${currentQuestions.length}`;
        questionOblast.textContent = question.oblast;
        questionText.textContent = question.pitanje;

        // Update progress bar
        progressBar.style.width = `${((currentQuestionIndex + 1) / currentQuestions.length) * 100}%`;

        // Create answer buttons with randomized order
        answersContainer.innerHTML = '';

        const answerMap = {
            'A': question.odgovor_a,
            'B': question.odgovor_b,
            'C': question.odgovor_c
        };

        // Use the pre-shuffled answer order for this question
        const answerOrder = question.answerOrder || ['A', 'B', 'C'];
        const displayLetters = ['A', 'B', 'C'];

        answerOrder.forEach((originalLetter, index) => {
            const displayLetter = displayLetters[index];
            const btn = document.createElement('button');
            btn.className = 'answer-btn';
            btn.dataset.originalLetter = originalLetter;

            if (userAnswers[currentQuestionIndex] === originalLetter) {
                btn.classList.add('selected');
            }

            btn.innerHTML = `
                <span class="answer-letter">${displayLetter}</span>
                <span class="answer-text">${answerMap[originalLetter]}</span>
            `;
            btn.addEventListener('click', () => selectAnswer(originalLetter, btn));
            answersContainer.appendChild(btn);
        });

        // Update navigation buttons
        updateNavigationButtons();
    }

    // Select an answer
    function selectAnswer(originalLetter, clickedBtn) {
        userAnswers[currentQuestionIndex] = originalLetter;

        // Update UI
        const buttons = answersContainer.querySelectorAll('.answer-btn');
        buttons.forEach(btn => {
            btn.classList.toggle('selected', btn === clickedBtn);
        });

        updateNavigationButtons();
    }

    // Update navigation button states
    function updateNavigationButtons() {
        prevBtn.disabled = currentQuestionIndex === 0;

        const isLastQuestion = currentQuestionIndex === currentQuestions.length - 1;
        const hasCurrentAnswer = userAnswers[currentQuestionIndex] !== null;

        if (isLastQuestion) {
            nextBtn.classList.add('hidden');
            submitBtn.classList.remove('hidden');
            submitBtn.disabled = !allQuestionsAnswered();
        } else {
            nextBtn.classList.remove('hidden');
            submitBtn.classList.add('hidden');
            nextBtn.disabled = !hasCurrentAnswer;
        }
    }

    // Check if all questions are answered
    function allQuestionsAnswered() {
        return userAnswers.every(answer => answer !== null);
    }

    // Navigate to previous question
    function goToPreviousQuestion() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion();
        }
    }

    // Navigate to next question
    function goToNextQuestion() {
        if (currentQuestionIndex < currentQuestions.length - 1) {
            currentQuestionIndex++;
            displayQuestion();
        }
    }

    // Submit the quiz and show results
    function submitQuiz() {
        const results = calculateResults();
        displayResults(results);
        showScreen(resultsScreen);
    }

    // Calculate quiz results
    function calculateResults() {
        let correct = 0;
        let incorrect = 0;
        const details = [];

        currentQuestions.forEach((question, index) => {
            const userAnswer = userAnswers[index];
            const isCorrect = userAnswer === question.tacan_odgovor;

            if (isCorrect) {
                correct++;
            } else {
                incorrect++;
            }

            details.push({
                question: question,
                userAnswer: userAnswer,
                isCorrect: isCorrect
            });
        });

        return {
            correct,
            incorrect,
            total: currentQuestions.length,
            percentage: Math.round((correct / currentQuestions.length) * 100),
            details
        };
    }

    // Display results
    function displayResults(results) {
        // Score circle
        document.getElementById('score-text').textContent = `${results.correct}/${results.total}`;

        // Score percentage with rating
        const percentageEl = document.getElementById('score-percentage');
        percentageEl.textContent = `${results.percentage}%`;
        percentageEl.className = 'score-percentage';

        if (results.percentage >= 90) {
            percentageEl.classList.add('excellent');
            percentageEl.textContent += ' - Odličan rezultat!';
        } else if (results.percentage >= 70) {
            percentageEl.classList.add('good');
            percentageEl.textContent += ' - Dobar rezultat';
        } else if (results.percentage >= 50) {
            percentageEl.classList.add('average');
            percentageEl.textContent += ' - Prosječan rezultat';
        } else {
            percentageEl.classList.add('poor');
            percentageEl.textContent += ' - Potrebno više učenja';
        }

        // Summary
        const summaryEl = document.getElementById('results-summary');
        summaryEl.innerHTML = `
            <div class="summary-item correct">
                <span class="count">${results.correct}</span>
                <span class="label">Tačnih odgovora</span>
            </div>
            <div class="summary-item incorrect">
                <span class="count">${results.incorrect}</span>
                <span class="label">Netačnih odgovora</span>
            </div>
        `;

        // Mistakes list with explanations
        const mistakesListEl = document.getElementById('mistakes-list');
        mistakesListEl.innerHTML = '';

        results.details.forEach((detail, index) => {
            const item = document.createElement('div');
            item.className = 'mistake-item' + (detail.isCorrect ? ' correct' : '');

            // Use the same answer order as displayed during the quiz
            const answerOrder = detail.question.answerOrder || ['A', 'B', 'C'];
            const displayLetters = ['A', 'B', 'C'];
            const answerMap = {
                'A': detail.question.odgovor_a,
                'B': detail.question.odgovor_b,
                'C': detail.question.odgovor_c
            };

            let answersHtml = answerOrder.map((originalLetter, index) => {
                const displayLetter = displayLetters[index];
                const isUserAnswer = originalLetter === detail.userAnswer;
                const isCorrectAnswer = originalLetter === detail.question.tacan_odgovor;

                let className = 'mistake-answer';
                let label = '';

                if (isUserAnswer && isCorrectAnswer) {
                    className += ' user-correct';
                    label = ' (Vaš odgovor)';
                } else if (isUserAnswer && !isCorrectAnswer) {
                    className += ' user-wrong';
                    label = ' (Vaš odgovor)';
                } else if (isCorrectAnswer) {
                    className += ' correct-answer';
                    label = ' (Tačan odgovor)';
                }

                return `
                    <div class="${className}">
                        <strong>${displayLetter}:</strong> ${answerMap[originalLetter]}${label}
                    </div>
                `;
            }).join('');

            item.innerHTML = `
                <div class="mistake-header">
                    <span>Pitanje ${index + 1}</span>
                    <span class="mistake-oblast">${detail.question.oblast}</span>
                </div>
                <p class="mistake-question">${detail.question.pitanje}</p>
                <div class="mistake-answers">
                    ${answersHtml}
                </div>
                <div class="mistake-explanation">
                    <strong>Objašnjenje:</strong>
                    <p>${detail.question.obrazlozenje}</p>
                </div>
            `;

            mistakesListEl.appendChild(item);
        });
    }

    // Get answer text by letter
    function getAnswerText(question, letter) {
        switch (letter) {
            case 'A': return question.odgovor_a;
            case 'B': return question.odgovor_b;
            case 'C': return question.odgovor_c;
            default: return '';
        }
    }

    // Restart quiz
    function restartQuiz() {
        showScreen(startScreen);
    }

    // Show specific screen, hide others
    function showScreen(screen) {
        startScreen.classList.add('hidden');
        quizScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');
        screen.classList.remove('hidden');

        // Scroll to top
        window.scrollTo(0, 0);
    }

    // Start the application
    document.addEventListener('DOMContentLoaded', init);
})();
