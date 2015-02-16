(ns server.handler
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            [me.raynes.conch :refer [programs with-programs let-programs] :as sh]
            [ring.middleware.defaults :refer [wrap-defaults site-defaults]]))

;; https://groups.google.com/forum/#!topic/clojure/UdFLYjLvNRs
(defn deep-merge
  "Recursively merges maps. If vals are not maps, the last value wins."
  [& vals]
  (if (every? map? vals)
    (apply merge-with deep-merge vals)
    (last vals)))

(defn modified-defaults []
  (deep-merge site-defaults {:security {:anti-forgery false}}))

(defroutes app-routes
  (GET "/" [] (slurp "resources/public/index.html"))
  (POST "/toJson" {body :body}
    (hash-map :status 200
              :headers {"Content-Type" "application/json"}
              :body
                (let-programs [as-json "../bin/toJson"]
                  (as-json {:in (slurp body)}))))
  (POST "/toMd" {body :body}
    (hash-map :status 200
              :headers {"Content-Type" "text/plain"}
              :body
                (let-programs [as-md "../bin/toMd"]
                  (as-md {:in (str (slurp body :encoding "UTF-8"))}))))
  (route/resources "/")
  (route/not-found "Not Found"))

(def app
  (wrap-defaults app-routes modified-defaults))
