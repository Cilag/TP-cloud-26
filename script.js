const API_URL = 'https://34.160.169.199.nip.io/api/hello';
const button = document.getElementById('callApiBtn');
const responseDiv = document.getElementById('response');
async function callApi() {
    button.disabled = true;
    button.textContent = 'Chargement...';
    responseDiv.style.display = 'none';
    responseDiv.classList.remove('error');
    
    try {
        const response = await fetch(API_URL, {
            method: 'GET'
        });
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        const data = await response.json();
        displayResponse(data, false);
        
    } catch (error) {
        console.error('Erreur lors de l\'appel API:', error);
        displayResponse({
            error: 'Impossible de contacter l\'API',
            details: error.message
        }, true);
    } finally {
        button.disabled = false;
        button.textContent = 'Appeler l\'API';
    }
}

function displayResponse(data, isError) {
    responseDiv.style.display = 'block';
    if (isError) {
        responseDiv.classList.add('error');
        responseDiv.innerHTML = `
            <strong>❌ Erreur</strong><br>
            ${data.error}<br>
            <small>${data.details}</small>
        `;
    } else {
        responseDiv.innerHTML = `
            <strong>✅ Réponse de l'API:</strong><br>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
    }
}

button.addEventListener('click', callApi);