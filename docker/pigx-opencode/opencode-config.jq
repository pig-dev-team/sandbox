def model_definition:
  {name: $name}
  + (if ($name | ascii_downcase | contains("deepseek"))
     then {reasoning: true, interleaved: {field: "reasoning_content"}}
     else {} end)
  + (if $limit > 0 then {limit: {context: 0, output: $limit}} else {} end);

{
  "$schema": "https://opencode.ai/config.json",
  model: ("pigx/" + $name),
  provider: {
    pigx: {
      npm: "@ai-sdk/openai-compatible",
      name: "PIGX",
      options: {baseURL: $url, apiKey: "{env:PIGX_MODEL_API_KEY}"},
      models: {($name): model_definition}
    }
  },
  enabled_providers: ["pigx"],
  permission: "allow",
  share: "disabled",
  autoupdate: false
}
