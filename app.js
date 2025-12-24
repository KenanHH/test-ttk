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
    const STATS_KEY = 'quiz_statistics';

    // State
    let allQuestions = [];
    let currentQuestions = [];
    let currentQuestionIndex = 0;
    let userAnswers = [];

    // DOM Elements
    const startScreen = document.getElementById('start-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const resultsScreen = document.getElementById('results-screen');
    const statsScreen = document.getElementById('stats-screen');
    const startBtn = document.getElementById('start-btn');
    const statsBtn = document.getElementById('stats-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const restartBtn = document.getElementById('restart-btn');
    const backFromStatsBtn = document.getElementById('back-from-stats-btn');
    const clearStatsBtn = document.getElementById('clear-stats-btn');
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
        statsBtn.addEventListener('click', showStats);
        prevBtn.addEventListener('click', goToPreviousQuestion);
        nextBtn.addEventListener('click', goToNextQuestion);
        submitBtn.addEventListener('click', submitQuiz);
        restartBtn.addEventListener('click', restartQuiz);
        backFromStatsBtn.addEventListener('click', () => showScreen(startScreen));
        clearStatsBtn.addEventListener('click', clearStats);
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
        // Use full question text to avoid collisions from truncation
        return `${question.oblast}:${question.pitanje}`;
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

        // Final safety check: remove any duplicates that slipped through
        const seenHashes = new Set();
        finalSelection = finalSelection.filter(q => {
            if (seenHashes.has(q.hash)) {
                console.warn('Duplicate question detected and removed:', q.pitanje.substring(0, 50));
                return false;
            }
            seenHashes.add(q.hash);
            return true;
        });

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
        saveTestResults(results);
        displayResults(results);
        showScreen(resultsScreen);
    }

    // Get statistics from localStorage
    function getStats() {
        try {
            const stats = localStorage.getItem(STATS_KEY);
            return stats ? JSON.parse(stats) : {
                totalTests: 0,
                totalCorrect: 0,
                totalQuestions: 0,
                testHistory: [],
                oblastStats: {}
            };
        } catch (e) {
            return {
                totalTests: 0,
                totalCorrect: 0,
                totalQuestions: 0,
                testHistory: [],
                oblastStats: {}
            };
        }
    }

    // Save statistics to localStorage
    function saveStats(stats) {
        try {
            localStorage.setItem(STATS_KEY, JSON.stringify(stats));
        } catch (e) {
            console.warn('Could not save statistics');
        }
    }

    // Save test results to statistics
    function saveTestResults(results) {
        const stats = getStats();

        // Update totals
        stats.totalTests++;
        stats.totalCorrect += results.correct;
        stats.totalQuestions += results.total;

        // Save test to history (keep last 50 tests)
        stats.testHistory.unshift({
            date: new Date().toISOString(),
            score: results.correct,
            total: results.total,
            percentage: results.percentage
        });
        if (stats.testHistory.length > 50) {
            stats.testHistory = stats.testHistory.slice(0, 50);
        }

        // Update oblast-specific stats
        results.details.forEach(detail => {
            const oblast = detail.question.oblast;
            if (!stats.oblastStats[oblast]) {
                stats.oblastStats[oblast] = {
                    correct: 0,
                    total: 0
                };
            }
            stats.oblastStats[oblast].total++;
            if (detail.isCorrect) {
                stats.oblastStats[oblast].correct++;
            }
        });

        saveStats(stats);
    }

    // Clear all statistics
    function clearStats() {
        if (confirm('Jeste li sigurni da želite obrisati svu statistiku? Ova akcija se ne može poništiti.')) {
            localStorage.removeItem(STATS_KEY);
            showStats(); // Refresh the stats display
        }
    }

    // Show statistics screen
    function showStats() {
        const stats = getStats();
        displayStats(stats);
        showScreen(statsScreen);
    }

    // Display statistics
    function displayStats(stats) {
        // Overall stats
        const avgScore = stats.totalTests > 0
            ? Math.round((stats.totalCorrect / stats.totalQuestions) * 100)
            : 0;

        document.getElementById('stats-total-tests').textContent = stats.totalTests;
        document.getElementById('stats-avg-score').textContent = avgScore + '%';
        document.getElementById('stats-total-questions').textContent = stats.totalQuestions;
        document.getElementById('stats-total-correct').textContent = stats.totalCorrect;

        // Oblast performance chart
        const chartContainer = document.getElementById('oblast-chart');
        chartContainer.innerHTML = '';

        if (Object.keys(stats.oblastStats).length === 0) {
            chartContainer.innerHTML = '<p class="no-data">Završite bar jedan test da vidite statistiku po oblastima.</p>';
        } else {
            // Sort by percentage (best to worst)
            const oblastData = REQUIRED_OBLASTI.map(oblast => {
                const data = stats.oblastStats[oblast] || { correct: 0, total: 0 };
                return {
                    name: oblast,
                    correct: data.correct,
                    total: data.total,
                    percentage: data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0
                };
            }).sort((a, b) => b.percentage - a.percentage);

            oblastData.forEach(oblast => {
                const bar = document.createElement('div');
                bar.className = 'chart-bar';

                let barClass = 'bar-fill';
                if (oblast.percentage >= 90) barClass += ' excellent';
                else if (oblast.percentage >= 75) barClass += ' very-good';
                else if (oblast.percentage >= 60) barClass += ' good';
                else if (oblast.percentage >= 40) barClass += ' average';
                else barClass += ' poor';

                bar.innerHTML = `
                    <div class="bar-label">
                        <span class="bar-name">${oblast.name}</span>
                        <span class="bar-stats">${oblast.correct}/${oblast.total} (${oblast.percentage}%)</span>
                    </div>
                    <div class="bar-track">
                        <div class="${barClass}" style="width: ${oblast.percentage}%"></div>
                    </div>
                `;
                chartContainer.appendChild(bar);
            });
        }

        // Recent tests
        const recentContainer = document.getElementById('recent-tests');
        recentContainer.innerHTML = '';

        if (stats.testHistory.length === 0) {
            recentContainer.innerHTML = '<p class="no-data">Još nema završenih testova.</p>';
        } else {
            const recentTests = stats.testHistory.slice(0, 10);
            recentTests.forEach((test, index) => {
                const testItem = document.createElement('div');
                testItem.className = 'recent-test-item';

                const date = new Date(test.date);
                const formattedDate = date.toLocaleDateString('bs-BA', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });

                let scoreClass = 'score-badge';
                if (test.percentage >= 90) scoreClass += ' excellent';
                else if (test.percentage >= 75) scoreClass += ' very-good';
                else if (test.percentage >= 60) scoreClass += ' good';
                else if (test.percentage >= 40) scoreClass += ' average';
                else scoreClass += ' poor';

                testItem.innerHTML = `
                    <span class="test-date">${formattedDate}</span>
                    <span class="${scoreClass}">${test.score}/${test.total} (${test.percentage}%)</span>
                `;
                recentContainer.appendChild(testItem);
            });
        }

        // Performance trend (last 10 tests)
        displayTrendChart(stats.testHistory.slice(0, 10).reverse());
    }

    // Display trend chart for recent tests
    function displayTrendChart(tests) {
        const trendContainer = document.getElementById('trend-chart');
        trendContainer.innerHTML = '';

        if (tests.length < 2) {
            trendContainer.innerHTML = '<p class="no-data">Potrebna su najmanje 2 testa za prikaz trenda.</p>';
            return;
        }

        const maxHeight = 100;
        const barWidth = Math.min(40, Math.floor(200 / tests.length));

        tests.forEach((test, index) => {
            const bar = document.createElement('div');
            bar.className = 'trend-bar';
            bar.style.width = barWidth + 'px';

            let barClass = 'trend-fill';
            if (test.percentage >= 90) barClass += ' excellent';
            else if (test.percentage >= 75) barClass += ' very-good';
            else if (test.percentage >= 60) barClass += ' good';
            else if (test.percentage >= 40) barClass += ' average';
            else barClass += ' poor';

            bar.innerHTML = `
                <div class="trend-value">${test.percentage}%</div>
                <div class="trend-track">
                    <div class="${barClass}" style="height: ${test.percentage}%"></div>
                </div>
                <div class="trend-label">#${index + 1}</div>
            `;
            trendContainer.appendChild(bar);
        });
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
        } else if (results.percentage >= 75) {
            percentageEl.classList.add('very-good');
            percentageEl.textContent += ' - Vrlo dobar rezultat!';
        } else if (results.percentage >= 60) {
            percentageEl.classList.add('good');
            percentageEl.textContent += ' - Dobar rezultat';
        } else if (results.percentage >= 40) {
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
        statsScreen.classList.add('hidden');
        screen.classList.remove('hidden');

        // Scroll to top
        window.scrollTo(0, 0);
    }

    // Start the application
    document.addEventListener('DOMContentLoaded', init);
})();
