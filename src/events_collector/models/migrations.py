from events_collector.config.log_conf import logger
from events_collector.models.base import SyncPostgresDriver


def apply_migrations():
    with SyncPostgresDriver().session() as db:
        db.execute("CREATE TYPE types AS ENUM ('FEMA', 'SEMA', 'MD5H', 'SHA1', 'SHA2', 'IP', 'URL', 'DOMAIN', 'FILE', 'REGISTRY');")
        db.execute('CREATE TABLE "indicators" ("id" SERIAL NOT NULL PRIMARY KEY, "type" types NOT NULL, "created_at" TIMESTAMP NOT NULL, "value" VARCHAR(256) NOT NULL, "context" JSONB NULL, "is_sending_to_detections" BOOLEAN DEFAULT TRUE, "is_false_positive" BOOLEAN DEFAULT FALSE, "weight" INTEGER NOT NULL DEFAULT 0, "is_archived" BOOLEAN DEFAULT TRUE, "false_detected_counter" INTEGER NOT NULL DEFAULT 0, "positive_detected_counter" INTEGER NOT NULL DEFAULT 0, "total_detected_counter" INTEGER NOT NULL DEFAULT 0, "first_detected_date" TIMESTAMP NULL, "last_detected_date" timestamp NULL, "updated_at" TIMESTAMP NOT NULL); ')
        db.execute('CREATE TABLE "stat_checked_objects" ("id" SERIAL NOT NULL PRIMARY KEY, "created_at" TIMESTAMP NOT NULL);')
        db.execute('CREATE TABLE "stat_matched_objects" ("id" SERIAL NOT NULL PRIMARY KEY, "created_at" TIMESTAMP NOT NULL, "indicator_id" INTEGER REFERENCES indicators(id));')
        db.execute('CREATE TABLE "detections" ("id" SERIAL NOT NULL PRIMARY KEY, "created_at" TIMESTAMP NOT NULL, "source_event" JSONB NULL, "indicator_id" INTEGER REFERENCES indicators(id), "detection_event" TEXT NULL);')

        db.flush()
        db.commit()
        logger.info("Migrations applied successfully...")
