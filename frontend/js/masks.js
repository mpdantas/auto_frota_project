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
 * Aplica uma máscara de Placa de Veículo (Mercosul/Antiga) a um campo de input.
 * Formatos: AAA-0A00 ou AAA0A00. Não é uma validação estrita, apenas formatação visual.
 *
 * @param {HTMLInputElement} inputElement O elemento input HTML.
 */
function applyPlacaMask(inputElement) {
    inputElement.addEventListener('input', function (e) {
        let value = e.target.value.toUpperCase(); // Converte para maiúsculas
        value = value.replace(/[^A-Z0-9]/g, ''); // Remove tudo que não for letra ou número

        // Limita a 7 caracteres (3 letras + 4 números/letra+números)
        if (value.length > 7) {
            value = value.substring(0, 7);
        }
        
        // Aplica o hífen
        // Exemplo: AAA-0000 ou AAA0A00
        if (value.length > 3) {
            // Se for placa Mercosul (AAA0A00)
            if (value.length >= 5 && isNaN(parseInt(value.charAt(4)))) { // Verifica se o 5º caractere é letra (índice 4)
                value = value.replace(/^([A-Z]{3})(\d{1})([A-Z]{1})(\d{0,2}).*/, '$1$2$3$4');
            }
            // Adiciona o hífen na 4ª posição (para AAA-0000 ou AAA0A00 quando completo)
            value = value.replace(/^([A-Z]{3}[0-9A-Z])([0-9A-Z]{3})$/, '$1-$2');
        }
        
        e.target.value = value;
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

        return `R$ <span class="math-inline">\{integerPart\},</span>{decimalPart}`;
    };

    // Função para obter o valor para o BACKEND (X.XXX.XX -> com ponto decimal)
    const getBackendValue = (displayValue) => {
        if (!displayValue) return '';
        // Remove "R$", pontos de milhar, e substitui vírgula por ponto
        return displayValue.replace('R$ ', '').replace(/\./g, '').replace(',', '.');
    };

    // Ao digitar no campo
    inputElement.addEventListener('input', function (e) {
        // Salva a posição do cursor para tentar restaurar (opcional, para melhor UX)
        // let oldCursorPos = e.target.selectionStart;
        // let oldValue = e.target.value;
        
        let displayValue = formatValueToDisplay(e.target.value);
        e.target.value = displayValue;

        // Tenta ajustar a posição do cursor (opcional, para melhor UX)
        // let newCursorPos = oldCursorPos + (displayValue.length - oldValue.length);
        // e.target.setSelectionRange(newCursorPos, newCursorPos);
    });

    // Ao sair do campo (para garantir formatação final)
    inputElement.addEventListener('blur', function (e) {
        e.target.value = formatValueToDisplay(e.target.value);
    });

    // Ao focar no campo (para remover formatação e facilitar a digitação)
    inputElement.addEventListener('focus', function (e) {
        // Remove a formatação para facilitar a digitação, mas mantém o valor puro de centavos
        let value = e.target.value;
        let cleaned = value.toString().replace(/[^0-9]/g, '');