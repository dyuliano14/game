// game_interaction.js - Script para interações do jogo
console.log("Game interaction script loaded at", new Date().toISOString());

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM carregado, configurando eventos");
    
    // Capturar cliques em botões de palavras
    document.addEventListener('click', function(e) {
        // Identificar botões de palavras clicadas
        if (e.target && e.target.tagName === 'BUTTON' && e.target.innerText.includes('👆')) {
            const word = e.target.innerText.replace('👆 ', '');
            console.log(`Palavra clicada: ${word}`);
        }
        
        // Identificar cliques em espaços em branco
        let target = e.target;
        while (target && target !== document) {
            if (target.classList && target.classList.contains('blank-word')) {
                const blankIndex = target.getAttribute('data-index');
                if (blankIndex) {
                    console.log(`Espaço em branco clicado: ${blankIndex}`);
                    handleBlankSpaceClick(blankIndex);
                }
                break;
            }
            target = target.parentElement;
        }
    });
});

// Configurar handlers para cliques
function setupClickHandlers() {
    // Delegação de eventos para capturar cliques nas áreas em branco
    document.body.addEventListener('click', function(e) {
        // Verificar se o clique foi em um elemento com classe blank-word
        let target = e.target;
        while (target && target !== document) {
            if (target.classList && target.classList.contains('blank-word')) {
                const blankIndex = target.getAttribute('data-index');
                if (blankIndex) {
                    handleBlankSpaceClick(blankIndex);
                }
                return;
            }
            target = target.parentElement;
        }
    });
}

// Quando um espaço em branco é clicado
function handleBlankSpaceClick(blankIndex) {
    console.log(`Espaço em branco clicado: ${blankIndex}`);
    
    // Verificar se temos uma palavra selecionada
    const params = new URLSearchParams(window.location.search);
    const selectedWord = params.get('selected_word');
    
    if (selectedWord) {
        console.log(`Enviando: palavra=${selectedWord}, índice=${blankIndex}`);
        
        // Configurar parâmetros
        const newParams = new URLSearchParams();
        newParams.set('selected_word', selectedWord);
        newParams.set('blank_index', blankIndex);
        
        // Adicionar timestamp para evitar cache do navegador
        newParams.set('_', Date.now());
        
        // Atualizar URL
        window.location.href = window.location.pathname + '?' + newParams.toString();
    } else {
        showToast("Selecione uma palavra primeiro!");
    }
}

// Exibir mensagem toast
function showToast(message) {
    // Criar elemento toast
    const toast = document.createElement('div');
    toast.className = 'game-toast';
    toast.textContent = message;
    
    // Adicionar ao documento
    document.body.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remover após alguns segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
}

// Adicionar estilos CSS personalizados
function addCustomStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .game-toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .game-toast.show {
            opacity: 1;
        }
        
        .filled-temp {
            background-color: #e9f7fd;
            border: 2px solid #90caf9;
        }
    `;
    document.head.appendChild(style);
}
