package com.project;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;
import java.util.HashMap;
import java.util.Map;

public class FuncaoQuatroHandler implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    private final DynamoDbClient dynamoDb = DynamoDbClient.create();
    private final String TABLE_NAME = "MARKET_LIST";

    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {
        Map<String, Object> response = new HashMap<>();

        try {
            String pk = (String) input.get("pk");
            String itemId = (String) input.get("itemId");

            if (pk == null || itemId == null) {
                response.put("status", "error");
                response.put("message", "Parâmetros 'pk' e 'itemId' são obrigatórios.");
                return response;
            }

            String composedPK = "LIST#" + pk;
            String composedSK = "ITEM#" + itemId;

            Map<String, AttributeValue> key = new HashMap<>();
            key.put("PK", AttributeValue.fromS(composedPK));
            key.put("SK", AttributeValue.fromS(composedSK));

            // Tentar deletar o item
            DeleteItemRequest deleteRequest = DeleteItemRequest.builder()
                    .tableName(TABLE_NAME)
                    .key(key)
                    .conditionExpression("attribute_exists(PK) AND attribute_exists(SK)")
                    .build();

            try {
                dynamoDb.deleteItem(deleteRequest);
                response.put("status", "success");
                response.put("message", "Item removido com sucesso.");
            } catch (ConditionalCheckFailedException e) {
                // Item já não existe — idempotente
                response.put("status", "success");
                response.put("message", "Item já estava removido.");
            }

        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", "Erro ao remover item: " + e.getMessage());
        }
        return response;
    }
}