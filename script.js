document.addEventListener('DOMContentLoaded', function () {
    let universitiesData = {};
    let searchResults = [];

    // Function to initialize the application
    function initializeApp() {
        Papa.parse('./results.csv', {
            download: true,
            header: true,
            dynamicTyping: true,
            complete: function (results) {
                universitiesData = organizeDataByUniversity(results.data);
                displayUniversityCards(Object.keys(universitiesData));
            }
        });
    }


    // Organize CSV data by university
    function organizeDataByUniversity(csvData) {
        let data = {};
        csvData.forEach(row => {
            if (!data[row.university_name]) {
                data[row.university_name] = {
                    reviews: [],
                    sentimentCounts: {
                        POSITIVE: 0,
                        NEGATIVE: 0,
                        NEUTRAL: 0,
                        MIXED: 0
                    },
                    keywords: new Set()
                };
            }
            data[row.university_name].reviews.push(row.text);
            data[row.university_name].sentimentCounts[row.sentiment]++;
            if (row.keywords) { // Check if keywords exist
                row.keywords.replace(/["']/g, "").split(",").forEach(keyword => {
                    data[row.university_name].keywords.add(keyword.trim());
                });
            }
        });
        return data;
    }

    // Function to display university cards
    function displayUniversityCards(universities) {
        const universityList = document.getElementById('universityList');
        universityList.innerHTML = '';

        universities.forEach(universityName => {
            const card = document.createElement('div');
            card.className = 'university-card';
            card.textContent = universityName;
            card.addEventListener('click', function () {
                displayUniversityDetails(universityName);
            });
            universityList.appendChild(card);
        });
    }

// Function to display university details
    function displayUniversityDetails(universityName) {
        const details = universitiesData[universityName];
        const modal = document.createElement('div');
        modal.className = 'modal';

        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        modalContent.innerHTML = `
    <span class="close">&times;</span>
    <h2>${universityName}</h2>
    <div class="content-container">
        <div class="chart-container">
            <canvas id="sentimentChart"></canvas>
        </div>
        <div class="keywords-container">
            <h3>Keywords</h3>
            <ul>${Array.from(details.keywords).map(keyword => `<li>${keyword}</li>`).join('')}</ul>
        </div>
    </div>
`;



        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        // Get the <span> element that closes the modal
        var span = modal.querySelector(".close");

        span.onclick = function() {
            modal.style.display = "none";
            modal.remove();
        };

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                modal.remove();
            }
        };

        modal.style.display = 'block';

        setTimeout(function() {
            createSentimentChart(details.sentimentCounts, 'sentimentChart');
        }, 0);
    }

    function createSentimentChart(sentimentCounts, canvasId) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Negative', 'Neutral', 'Mixed'],
                datasets: [{
                    label: 'Sentiment Analysis',
                    data: [
                        sentimentCounts.POSITIVE,
                        sentimentCounts.NEGATIVE,
                        sentimentCounts.NEUTRAL,
                        sentimentCounts.MIXED
                    ],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255,99,132,1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });
    }



    // Function to calculate sentiment percentage
    function calculateSentimentPercentage(count, total) {
        return ((count / total) * 100).toFixed(2);
    }

    // Event listener for the search bar
    document.getElementById('searchBar').addEventListener('input', function (e) {
        const searchTerm = e.target.value.toLowerCase();
        searchResults = Object.keys(universitiesData).filter(universityName =>
            universityName.toLowerCase().includes(searchTerm)
        );
        displayUniversityCards(searchResults);
    });

    // Initialize the application
    initializeApp();
});
