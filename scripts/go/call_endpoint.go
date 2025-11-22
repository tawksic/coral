package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

var SCHEME = "http"
var HTTP_TIMEOUT = 10 * time.Second
var OPENAPIURL = "http://localhost:80/openapi.json"

// OpenAPI spec structure - documents the API schema
type OpenAPISpec struct {
	Paths map[string]PathItem `json:"paths"`
}

type PathItem struct {
	Get    *Operation `json:"get,omitempty"`
	Post   *Operation `json:"post,omitempty"`
	Put    *Operation `json:"put,omitempty"`
	Delete *Operation `json:"delete,omitempty"`
	Patch  *Operation `json:"patch,omitempty"`
}

type Operation struct {
	Parameters []Parameter `json:"parameters,omitempty"`
}

type Parameter struct {
	Name     string      `json:"name"`
	Required bool        `json:"required"`
	Schema   ParamSchema `json:"schema"`
}

type ParamSchema struct {
	Type    string `json:"type"`
	Maximum *int   `json:"maximum,omitempty"`
}

func formatURL(endpoint string, params string, baseURL string) string {
	var rawURL url.URL
	rawURL.Scheme = SCHEME
	rawURL.Host = baseURL

	if !strings.HasPrefix(endpoint, "/") {
		rawURL.Path = "/" + endpoint
	} else {
		rawURL.Path = endpoint
	}

	if params == "" {
		return rawURL.String()
	}

	rawQuery := rawURL.Query()
	for _, pair := range strings.Split(params, ",") {
		parts := strings.Split(pair, "=")
		if len(parts) != 2 {
			fmt.Printf("Invalid params: %v\n\n", pair)
			printHelp()
			os.Exit(1)
		}
		rawQuery.Set(parts[0], parts[1])
	}
	rawURL.RawQuery = rawQuery.Encode()

	return rawURL.String()
}

func fetchOpenAPISpec() OpenAPISpec {
	client := &http.Client{Timeout: HTTP_TIMEOUT}
	resp, err := client.Get(OPENAPIURL)
	if err != nil {
		log.Fatalf("Failed to fetch OpenAPI spec from %s: %v", OPENAPIURL, err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Failed to read OpenAPI spec: %v", err)
	}

	var spec OpenAPISpec
	if err := json.Unmarshal(body, &spec); err != nil {
		log.Fatalf("Failed to parse OpenAPI spec: %v", err)
	}

	return spec
}

func printParam(param Parameter) {
	requiredStr := ""
	if param.Required {
		requiredStr = " (required)"
	}

	maxStr := ""
	if param.Schema.Maximum != nil {
		maxStr = fmt.Sprintf(", max: %d", *param.Schema.Maximum)
	}

	fmt.Printf("  - %s (%s%s)%s\n", param.Name, param.Schema.Type, maxStr, requiredStr)
}

func printOperation(method string, path string, op *Operation) {
	if op == nil {
		return
	}

	fmt.Printf("%s %s\n", method, path)
	for _, param := range op.Parameters {
		printParam(param)
	}
}

func printHelp() {
	spec := fetchOpenAPISpec()

	fmt.Println("Available endpoints:")
	fmt.Println()

	for path, pathItem := range spec.Paths {
		printOperation("GET", path, pathItem.Get)
		printOperation("POST", path, pathItem.Post)
		printOperation("PUT", path, pathItem.Put)
		printOperation("DELETE", path, pathItem.Delete)
		printOperation("PATCH", path, pathItem.Patch)
	}
}

func main() {
	endpoint := flag.String("endpoint", "/health", "the endpoint you want to call")
	params := flag.String("params", "", "Query parameters as key=value pairs, comma-separated (e.g., duration=10,delay=1)")
	baseURL := flag.String("url", "localhost:80", "Base URL for the API")
	help := flag.Bool("eh", false, "Show 'endpoint help'")
	flag.Parse()

	if *help {
		printHelp()
		os.Exit(0)
	}

	formattedURL := formatURL(*endpoint, *params, *baseURL)

	client := &http.Client{Timeout: HTTP_TIMEOUT}
	resp, err := client.Get(formattedURL)
	if err != nil {
		log.Fatalf("Error calling %v: %v", formattedURL, err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response: %v", err)
	}

	fmt.Println(string(body))
}
