package main.java.com.project;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

public class FuncaoUmHandler implements RequestHandler<Object, String> {

    @Override
    public String handleRequest(Object input, Context context){
         var logger = context.getLogger();
         logger.log("Request received: " + input);

         return """
                     {
                        "statusCode": 200,
                        "body": "Hellow Terraform"
                     }
                     """;
    }
}