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
        // Remove tudo que não for dígito
        value = value.replace(/\D/g, '');

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

// Quando o DOM estiver completamente carregado, aplica as máscaras
document.addEventListener('DOMContentLoaded', function() {
    // Encontra o campo de CNPJ pelo seu ID ou name
    // O Django Forms geralmente dá aos campos um ID no formato 'id_nome_do_campo'
    const cnpjInput = document.getElementById('id_cnpj'); 
    
    if (cnpjInput) {
        applyCnpjMask(cnpjInput);
    }
});