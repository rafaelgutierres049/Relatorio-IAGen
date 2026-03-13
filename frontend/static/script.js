document.addEventListener("DOMContentLoaded", function() {
    // Função para comparar os valores e aplicar as classes
    function compareValues(id1, id2) {
        var value1 = document.getElementById(id1).innerText.trim();
        var value2 = document.getElementById(id2).innerText.trim();

        // Verifica se algum dos valores é 'N/A'
        if (value1 === 'N/A') {
            value1 = 0;
            return;
        }

        // Converte os valores para números, removendo caracteres não numéricos
        var numValue1 = parseFloat(value1.replace(/[^0-9.-]/g, ''));
        var numValue2 = parseFloat(value2.replace(/[^0-9.-]/g, ''));

    

        // Aplica as classes com base na comparação
        if (numValue1 > numValue2) {
            document.getElementById(id1).classList.add('better');
            document.getElementById(id2).classList.add('worse');
        } else if (numValue1 < numValue2) {
            document.getElementById(id1).classList.add('worse');
            document.getElementById(id2).classList.add('better');
        }
    }

    // Compare os valores das diferentes métricas
    compareValues('preco-ticker1', 'preco-ticker2');
    compareValues('pl-ticker1', 'pl-ticker2');
    compareValues('dividend-ticker1', 'dividend-ticker2');
    compareValues('variacao-semana-ticker1', 'variacao-semana-ticker2');
    compareValues('variacao-mes-ticker1', 'variacao-mes-ticker2');
    compareValues('variacao-ano-ticker1', 'variacao-ano-ticker2');
});
