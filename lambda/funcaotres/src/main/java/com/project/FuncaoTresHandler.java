package com.project;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.List;

public class FuncaoTresHandler implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    private final DynamoDbClient dynamoDb = DynamoDbClient.create();
    private static final String TABLE = "MARKET_LIST";

    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {
        try {
            // Extrai parâmetros
            var pathParams = (Map<String, String>) input.get("pathParameters");
            var body = (Map<String, String>) input.get("body");

            // Validações básicas
            if (body.values().stream().allMatch(v -> v == null)) {
                throw new RuntimeException("Forneça pelo menos um campo para atualização");
            }
            if (body.get("status") != null && !List.of("TODO", "DONE").contains(body.get("status"))) {
                throw new RuntimeException("Status deve ser 'TODO' ou 'DONE'");
            }

            // Prepara chave e verifica existência
            var key = Map.of(
                    "PK", attr("LIST#" + pathParams.get("listId")),
                    "SK", attr("ITEM#" + pathParams.get("itemId"))
            );

            if (!dynamoDb.getItem(b -> b.tableName(TABLE).key(key)).hasItem()) {
                throw new RuntimeException("Item não encontrado");
            }

            // Prepara atributos para atualização
            var updateData = filterNonNull(body);

            // Executa atualização
            var response = dynamoDb.updateItem(b -> b
                    .tableName(TABLE)
                    .key(key)
                    .updateExpression("SET " + String.join(", ", updateData.expressions))
                    .expressionAttributeNames(updateData.attributeNames)
                    .expressionAttributeValues(updateData.attributeValues)
                    .returnValues(ReturnValue.ALL_NEW)
            );

            // Converte resposta
            return response.attributes().entrySet().stream()
                    .collect(Collectors.toMap(
                            Map.Entry::getKey,
                            e -> convertAttribute(e.getValue())
                    ));

        } catch (Exception e) {
            throw new RuntimeException("Falha na atualização: " + e.getMessage(), e);
        }
    }

    // Classe para agrupar dados de atualização
    private static class UpdateData {
        List<String> expressions;
        Map<String, String> attributeNames;
        Map<String, AttributeValue> attributeValues;
    }

    // Filtra campos não nulos e prepara estruturas para atualização
    private UpdateData filterNonNull(Map<String, String> body) {
        UpdateData data = new UpdateData();

        data.attributeNames = new HashMap<>();
        data.attributeValues = new HashMap<>();
        data.expressions = body.entrySet().stream()
                .filter(e -> e.getValue() != null)
                .map(e -> {
                    String attrName = "#" + e.getKey();
                    String valueKey = ":" + e.getKey();

                    data.attributeNames.put(attrName, e.getKey());
                    data.attributeValues.put(valueKey, attr(e.getValue()));

                    return attrName + " = " + valueKey;
                })
                .collect(Collectors.toList());

        return data;
    }

    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }

    private Object convertAttribute(AttributeValue attr) {
        if (attr.s() != null) return attr.s();
        if (attr.n() != null) return attr.n();
        if (attr.bool() != null) return attr.bool();
        if (attr.hasM()) return attr.m().entrySet().stream()
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        e -> e.getValue().s()
                ));
        return null;
    }
}