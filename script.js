// 🌐 Dropdown Menu Toggle
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    } else {
        dropdown.style.display = 'block';
    }
}

// 🛑 Close Dropdown when Clicking Outside
window.onclick = function(event) {
    if (!event.target.matches('button')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            dropdowns[i].style.display = "none";
        }
    }
};

// ✅ Registration Form Submission
const joinForm = document.getElementById('joinForm');
if (joinForm) {
    joinForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value.trim();
        const year = document.getElementById('year').value;
        const experience = document.getElementById('experience').value.trim();
        const reason = document.getElementById('reason').value.trim();

        const formData = {
            name: name,
            year: year,
            experience: experience,
            reason: reason,
            club: 'Web Development'  // Change if needed
        };

        fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            showTemporaryMessage(data.message, 3000);
            setTimeout(() => {
                joinForm.reset();
            }, 3000);  // Reset only after 3 seconds
            console.log(data);
        })
        .catch(error => {
            console.error('❌ Error:', error);
            showTemporaryMessage('Error submitting form.', 3000);
        });
    });
}

// 💬 Message Function with Fade-In & Fade-Out
function showTemporaryMessage(message, duration) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.left = '50%';
    messageDiv.style.transform = 'translateX(-50%)';
    messageDiv.style.background = '#2e7d32';  // Dark green for better visibility
    messageDiv.style.color = '#fff';
    messageDiv.style.padding = '14px 28px';
    messageDiv.style.borderRadius = '10px';
    messageDiv.style.fontSize = '17px';
    messageDiv.style.fontWeight = '600';
    messageDiv.style.boxShadow = '0 4px 10px rgba(0,0,0,0.25)';
    messageDiv.style.opacity = '0';
    messageDiv.style.transition = 'opacity 0.4s ease';
    messageDiv.style.zIndex = '10000';
    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.style.opacity = '1';
    }, 50);

    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.remove();
        }, 400);
    }, duration);
}
