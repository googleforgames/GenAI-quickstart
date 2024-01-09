
## Friends Chat Demo App

This demo app is our "hello world" example. By default, the application 
starts a chat with a popular video game character, Mario from Super Mario Bros.

You're able to ask questions within the chat and the character will respond. 

Additionally, you can also add you own character, by inviting them to the chat. 
You can invite a new character to the chat by saying something such as this: 

```
"Can you add X from the video game Y."

For example:
Can you add Luigi from the video game Super Mario Bros
```

### To deploy the demo app, run the following:

```
cd $CUR_DIR/examples/friendschat

export PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)

find . -type f -name "*.yaml" -exec sed -i "s:your-unique-project-id:$PROJECT_ID:g" {} +

skaffold run
```

