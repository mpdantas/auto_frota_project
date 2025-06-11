// frontend/js/masks.js

/**
 * Aplica uma máscara de CNPJ a um campo de input.
 * Formato: XX.XXX.XXX/YYYY-ZZ
 *
 * @param {HTMLInputElement} inputElement O elemento input HTML ao qual a máscara será aplicada.
 */
function applyCnpjMask(inputElement) {
    inputElement.addEventListener('input', function (e) {
        let value = e.target.value;
        value = value.replace(/\D/g, ''); // Remove tudo que não for dígito

        // Aplica a máscara
        if (value.length > 12) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{0,2}).*/, '$1.$2.$3/$4-$5');
        } else if (value.length > 8) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{0,4}).*/, '$1.$2.$3/$4');
        } else if (value.length > 5) {
            value = value.replace(/^(\d{2})(\d{3})(\d{0,3}).*/, '$1.$2.$3');
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,3}).*/, '$1.$2');
        }
        e.target.value = value;
    });
}

/**
 * Aplica uma máscara de Placa de Veículo a um campo de input.
 * Tenta ajustar para padrões AAA-NNNN ou AAA0A00.
 *
 * @param {HTMLInputElement} inputElement O elemento input HTML.
 */
function applyPlacaMask(inputElement) {
    inputElement.addEventListener('input', function (e) {
        let value = e.target.value.toUpperCase(); // Converte para maiúsculas logo no início
        let cleanValue = value.replace(/[^A-Z0-9]/g, ''); // Remove tudo que não for letra ou número (e hífen, por enquanto)

        let formattedValue = cleanValue;

        // Limita a 7 caracteres alfanuméricos
        if (cleanValue.length > 7) {
            cleanValue = cleanValue.substring(0, 7);
        }

        // --- Lógica de Formatação da Placa ---
        // Se a placa tem 7 caracteres alfanuméricos
        if (cleanValue.length === 7) {
            // Padrão antigo: AAA-NNNN
            if (/^[A-Z]{3}\d{4}$/.test(cleanValue)) {
                formattedValue = cleanValue.replace(/^([A-Z]{3})(\d{4})$/, '$1-$2');
            }
            // Padrão Mercosul: AAA0A00 (mantém sem hífen)
            else if (/^[A-Z]{3}\d[A-Z]\d{2}$/.test(cleanValue)) {
                formattedValue = cleanValue;
            } else {
                // Se chegou a 7 caracteres e não é nenhum dos padrões, mantém como está
                formattedValue = cleanValue;
            }
        } else if (cleanValue.length >= 4) {
            // Durante a digitação, se o 4º caractere é um número (índice 3 na string limpa),
            // e a placa está no meio de formação, tenta adicionar o hífen para o padrão antigo
            if (!isNaN(parseInt(cleanValue.charAt(3)))) {
                 formattedValue = cleanValue.replace(/^([A-Z]{3})([0-9].*)/, '$1-$2');
            } else {
                // Se o 4º caractere é uma letra (Mercosul), mantém sem hífen por enquanto
                formattedValue = cleanValue;
            }
        } else {
            formattedValue = cleanValue;
        }

        e.target.value = formattedValue;
    });
}


/**
 * Aplica uma máscara de RENAVAM (11 dígitos) a um campo de input.
 * Formato: 00000000000 (apenas números)
 *
 * @param {HTMLInputElement} inputElement O elemento input HTML.
 */
function applyRenavamMask(inputElement) {
    inputElement.addEventListener('input', function (e) {
        let value = e.target.value;
        value = value.replace(/\D/g, ''); // Remove tudo que não for dígito
        if (value.length > 11) { // Limita a 11 dígitos
            value = value.substring(0, 11);
        }
        e.target.value = value;
    });
}

/**
 * Aplica uma máscara de valor monetário (Franquia) a um campo de input.
 * Formato de exibição: R$ X.XXX,XX
 * Formato para o backend: XXXXX.XX (com ponto decimal)
 *
 * @param {HTMLInputElement} inputElement O elemento input HTML ao qual a máscara será aplicada.
 */
function applyFranquiaMask(inputElement) {
    // Função para formatar o valor NUMÉRICO para exibição (R$ X.XXX,XX)
    const formatValueToDisplay = (value) => {
        // Converte o valor para string, remove R$, pontos e vírgulas para ter apenas dígitos
        let clean = value.toString().replace(/[^0-9]/g, '');
        if (clean === '') return '';

        // Adiciona zeros à esquerda se for muito pequeno para ter centavos
        while (clean.length < 3) {
            clean = '0' + clean;
        }

        // Formata para R$ X.XXX,XX
        let integerPart = clean.substring(0, clean.length - 2);
        let decimalPart = clean.substring(clean.length - 2);

        // Adiciona separador de milhares (ponto)
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

        return `R$ ${integerPart},${decimalPart}`;
    };

    // Função para obter o valor para o BACKEND (X.XXX.XX -> com ponto decimal)
    const getBackendValue = (displayValue) => {
        if (!displayValue) return '';
        // Remove "R$", pontos de milhar, e substitui vírgula por ponto
        return displayValue.replace('R$ ', '').replace(/\./g, '').replace(',', '.');
    };

    // Ao digitar no campo
    inputElement.addEventListener('input', function (e) {
        let displayValue = formatValueToDisplay(e.target.value);
        e.target.value = displayValue;
    });

    // Ao sair do campo (para garantir formatação final)
    inputElement.addEventListener('blur', function (e) {
        e.target.value = formatValueToDisplay(e.target.value);
    });

    // Ao focar no campo (para remover formatação e facilitar a digitação)
    inputElement.addEventListener('focus', function (e) {
        let value = e.target.value;
        let cleaned = value.toString().replace(/[^0-9]/g, '');
        e.target.value = cleaned; 
    });

    // Antes do formulário ser submetido, transforma o valor para o formato do backend
    if (inputElement.form) {
        inputElement.form.addEventListener('submit', function () {
            inputElement.value = getBackendValue(inputElement.value);
        });
    }

    // Garante que o valor inicial (se já existir, ex: na edição) seja formatado ao carregar
    if (inputElement.value) {
        let initialCleanValue = inputElement.value.toString().replace(/[^0-9.]/g, ''); 
        if (initialCleanValue) {
            let parts = initialCleanValue.split('.');
            let integerPart = parts[0] || '0';
            let decimalPart = parts[1] || '00';
            let valueInCents = integerPart + decimalPart.padEnd(2, '0').substring(0,2); 

            inputElement.value = formatValueToDisplay(valueInCents);
        }
    }
}

/**
 * Aplica uma máscara que converte todo o texto de um input para maiúsculas.
 *
 * @param {HTMLInputElement} inputElement O elemento input HTML ao qual a máscara será aplicada.
 */
function applyUppercaseMask(inputElement) {
    inputElement.addEventListener('input', function (e) {
        e.target.value = e.target.value.toUpperCase(); // Converte para maiúsculas
    });
}


// Quando o DOM estiver completamente carregado, aplica as máscaras
document.addEventListener('DOMContentLoaded', function() {
    // --- Aplicação das Máscaras de Input ---
    // CNPJ (na página de registro de empresa)
    const cnpjInput = document.getElementById('id_cnpj'); 
    if (cnpjInput) {
        applyCnpjMask(cnpjInput);
    }

    // Placa (na página de registro/edição de veículo)
    const placaInput = document.getElementById('id_placa');
    if (placaInput) {
        applyPlacaMask(placaInput);
    }

    // Renavam (na página de registro/edição de veículo)
    const renavamInput = document.getElementById('id_renavam');
    if (renavamInput) {
        applyRenavamMask(renavamInput);
    }

    // Franquia (na página de registro/edição de veículo)
    const franquiaInput = document.getElementById('id_franquia');
    if (franquiaInput) {
        applyFranquiaMask(franquiaInput);
    }

    // Chassi (na página de registro/edição de veículo)
    const chassiInput = document.getElementById('id_chassi');
    if (chassiInput) {
        applyUppercaseMask(chassiInput); // Aplica a nova máscara de maiúsculas
    }

    // --- Lógica para Mensagens Auto-ocultáveis (Toasts) ---
    const messageContainer = document.querySelector('.messages-container');
    if (messageContainer) {
        const messages = messageContainer.querySelectorAll('li[data-autohide="true"]');
        messages.forEach(message => {
            // Define um timer para a mensagem desaparecer
            setTimeout(() => {
                message.classList.add('fade-out'); // Adiciona a classe para iniciar a transição
                // Remove a mensagem do DOM após a transição
                message.addEventListener('transitionend', () => message.remove());
            }, 5000); // 5000 milissegundos = 5 segundos

            // Adiciona listener para o botão de fechar manualmente
            const closeBtn = message.querySelector('.close-btn');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    message.classList.add('fade-out');
                    message.addEventListener('transitionend', () => message.remove());
                });
            }
        });
    }
});