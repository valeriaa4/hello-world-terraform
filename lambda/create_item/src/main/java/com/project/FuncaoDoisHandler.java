package com.project;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

public class FuncaoDoisHandler implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    private final DynamoDbClient dynamoDbClient = DynamoDbClient.create();
    private final String TABLE_NAME = System.getenv("MARKET_LIST");
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {

        try {

            String name = (String) input.get("name");
            String date = (String) input.get("date");
            String itemId = UUID.randomUUID().toString();

            // formatando PK e SK
            String pk = "LIST#" + date.replace("-", "");
            String sk = "ITEM#" + itemId;

            // criação do item
            Map<String, AttributeValue> item = new LinkedHashMap<>();
            item.put("PK", AttributeValue.fromS(pk));
            item.put("SK", AttributeValue.fromS(sk));
            item.put("itemId", AttributeValue.fromS(itemId));
            item.put("name", AttributeValue.fromS(name));
            item.put("date", AttributeValue.fromS(date));
            item.put("status", AttributeValue.fromS("todo"));
            item.put("entityType", AttributeValue.fromS("Item"));

            // colocando no dynamo
            PutItemRequest request = PutItemRequest.builder()
                    .tableName(TABLE_NAME)
                    .item(item)
                    .build();

            dynamoDbClient.putItem(request);

            // exibir mensagem
            Map<String, Object> response = new LinkedHashMap<>();
            response.put("status", "sucesso");
            response.put("item", Map.of(
                    "PK", pk,
                    "SK", sk,
                    "itemId", itemId,
                    "name", name,
                    "date", date,
                    "status", "todo",
                    "entityType", "Item"
            ));
            return response;
        } catch (Exception e) {
            return Map.of(
                    "error", "Erro ao criar item: " + e.getMessage()
            );
        }
    }
}