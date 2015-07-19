(ns project-md.core-test
  (:require [clojure.test :refer :all]
            [me.raynes.fs :as fs]
            [me.raynes.conch :refer [programs with-programs let-programs] :as sh]
            ))


(defn toMd [input]
  (let-programs [md "bin/toMd"]
    (md {:in input}))
)

(defn toJson [input]
  (let-programs [json "bin/toJson"]
    (json {:in input}))
)


(doseq [f (fs/list-dir "./test/resources/dirtymd")]
  (when (fs/file? f)
    (eval
      `(deftest ~(symbol (str "dirty-md-to-json-" (fs/name f)))
        (println "Test [dmd -> json]" ~(.getName f))
        (let [f# (fs/file ~(.getPath f))
              md# (slurp f#)
              json# (toJson md#)
              fname# (fs/name f#)
              ejson# (slurp (str "./test/resources/json/" fname#))]
          (is (= json# ejson#)))
      )))
)

(doseq [f (fs/list-dir "./test/resources/md")]
  (when (fs/file? f)
    (eval
      `(deftest ~(symbol (str "md-to-json-" (fs/name f)))
        (println "Test [md -> json]" ~(.getName f))
        (let [f# (fs/file ~(.getPath f))
              md# (slurp f#)
              json# (toJson md#)
              fname# (fs/name f#)
              ejson# (slurp (str "./test/resources/json/" fname#))]
          (is (= json# ejson#)))
      )))
)

(doseq [f (fs/list-dir "./test/resources/json")]
  (when (fs/file? f)
    (eval
      `(deftest ~(symbol (str "json-to-md-" (fs/name f)))
        (println "Test [json -> md]" ~(.getName f))
        (let [f# (fs/file ~(.getPath f))
              json# (slurp f#)
              md# (toMd json#)
              fname# (fs/name f#)
              emd# (slurp (str "./test/resources/md/" fname#))]
          (is (= md# emd#)))
      )))
)



