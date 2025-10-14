import docker

def get_container_stats():
    """Helper function to get the current container"""
    client = docker.from_env()
    try:
        container = client.containers.get("coral-api-1")
        stats = container.stats(stream=False)
        return stats
    except Exception as e:
        print(f"Error getting container: {e}")
        return None


def get_container_memory():
    """Get memory statistics for the container"""
    stats = get_container_stats()
    if not stats:
        return None

    try:
        memory_stats = stats.get("memory_stats")

        if memory_stats:
            usage_bytes = memory_stats.get("usage")
            limit_bytes = memory_stats.get("limit")
        else:
            return None

        if usage_bytes is not None and limit_bytes is not None:
            # Convert bytes to MiB for readability
            usage_mib = usage_bytes / (1024 * 1024)
            limit_mib = limit_bytes / (1024 * 1024)
            percentage = (usage_mib / limit_mib * 100) if limit_mib > 0 else 0

            return {
                'usage_mib': round(usage_mib, 2),
                'limit_mib': round(limit_mib, 2),
                'percentage': round(percentage, 2)
            }

        return None

    except Exception as e:
        print(f"An error occurred getting memory stats: {e}")
        return None


def get_container_cpu():
    """Get CPU statistics for the container"""
    stats = get_container_stats()
    if not stats:
        return None

    try:
        cpu_stats = stats.get("cpu_stats")
        if not cpu_stats:
            return None

        # Convert nanoseconds to more readable units
        total_usage_ns = cpu_stats["cpu_usage"]["total_usage"]
        total_usage_seconds = total_usage_ns / 1_000_000_000  # Convert to seconds

        return {'total_usage_seconds': round(total_usage_seconds, 2)}

    except Exception as e:
        print(f"An error occurred getting CPU stats: {e}")
        return None

